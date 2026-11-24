# Comparação de agendadores para o módulo Varredura (LhamaLog)

> Pesquisa verificada na web em 14/10/2026. É material de apoio: a decisão fica com o Michel (não é um ADR).
> Legenda: **[INFERIDO]** = conclusão de análise, sem afirmação direta na fonte · **[PENDENTE]** = precisa de validação (PoC ou consulta ao fornecedor).

## Contexto
- Stack: Java 25, Spring Boot 4.1.1, Maven, MongoDB (banco principal), Redis Streams (filas), serviços distribuídos com várias instâncias.
- Varredura: roda por produto, num cron definido pelo cliente (dinâmico, por tenant), mais um gatilho opcional por tamanho de fila (padrão 500), DLQ após 3 tentativas, lock chave-valor no MongoDB com TTL, histórico de 3 meses.

## Tabela comparativa

| Critério | JobRunr (OSS 8.x / Pro 9.x) | Quartz 2.5.x | Spring `@Scheduled` / `TaskScheduler` + ShedLock 7.x |
|---|---|---|---|
| Spring Boot 4 | Sim. `jobrunr-spring-boot-4-starter` desde a v8.3; Pro tem `jobrunr-pro-spring-boot-4-starter` (9.0.1) | Sim. `spring-boot-starter-quartz` com autoconfiguração no Boot 4.1.1 | Sim. É nativo do Spring Framework 7; ShedLock 7.x é testado com Boot 4.x |
| Armazenamento no MongoDB | **Sim, nativo** (`MongoDBStorageProvider`, Mongo 4 ou superior; exige leitura no primário e configuração de UUID) | **Não oficial.** Só JDBC (relacional). Para Mongo existe o `quartz-mongodb` de terceiros (2.2.0-rc2, pouco mantido) | Lock no Mongo via `shedlock-provider-mongo`. Os schedules ficam numa coleção própria **[INFERIDO]** |
| Redis | **Removido na v8** (sem storage em Redis) | Não | Sim, via `shedlock-provider-redis-spring` (só para o lock) |
| Licença / custo | OSS: LGPL 3.0, gratuito. Pro Business: cerca de €850 por mês por cluster de produção; Enterprise: ilimitado | Apache 2.0, gratuito | Apache 2.0, gratuito |
| Limites da versão gratuita | Cerca de 100 jobs recorrentes por banco (limite técnico, não contratual). Sem timeouts, mutex, filas dinâmicas por tenant, rate limit nem reprocessamento de execuções perdidas (tudo isso é Pro) | Sem limites de recursos | Sem limites |
| Cluster / sem execução duplicada | Sim: coordenação pelo storage e, por padrão, sem execução concorrente do mesmo job recorrente | Sim, com JDBC JobStore `isClustered=true` (exige banco relacional) | ShedLock garante "no máximo uma execução ao mesmo tempo" (não é um scheduler: o lock é por nome de task e expira por `lockAtMostFor`) |
| Schedules dinâmicos por tenant em tempo de execução | Sim: `scheduleRecurrently(id, cron, ...)` por API. **Mas 1 produto = 1 job recorrente, o que estoura cerca de 100 no OSS** **[INFERIDO]** | Sim, de forma madura (triggers criados e alterados por API, persistidos) | Possível com `TaskScheduler.schedule(task, CronTrigger)`, mas o registro, a recarga após restart e a distribuição entre instâncias ficam por nossa conta **[INFERIDO]** |
| Retentativas / DLQ | Retry automático com backoff exponencial (o padrão é 10 tentativas, configurável). O estado "Failed" funciona como uma DLQ **[INFERIDO]** | Sem retry nativo (feito à mão via `JobExecutionException`/listeners) | Sem retry nativo (Spring Retry/Resilience4j ou a própria DLQ no Redis Streams) |
| Dashboard | Sim (simples no OSS, avançado no Pro) | Não (só ferramentas de terceiros) | Não (Actuator `/scheduledtasks` apenas lista as tasks) |
| Gatilho por tamanho de fila (500) | Por fora: um consumidor/monitor enfileira um job (`enqueue`) **[INFERIDO]** | Por fora: `triggerJob` sob demanda **[INFERIDO]** | Por fora: um monitor chama a execução diretamente **[INFERIDO]** |
| Histórico de 3 meses | O storage tem política de exclusão de jobs concluídos, mas o histórico de negócio deve ficar no Mongo próprio **[INFERIDO]** | Não guarda histórico | Não guarda histórico |
| Maturidade | Ativo (v8.3 a 9.0.1 em 2026), empresa por trás | Muito maduro, mas com lançamentos esparsos (2.5.2 em 01/12/2025) | Spring: maduro. ShedLock: muito ativo (7.10.1 em 09/09/2026), cerca de 4,2 mil estrelas |
| Novo componente de infra | Nenhum (usa o Mongo) | **Exige um banco relacional** (ou um store Mongo de terceiros) | Nenhum |

## Leitura dos critérios para a Varredura
- **Quartz** é o mais completo como scheduler dinâmico, mas obriga a adicionar PostgreSQL/MySQL só para ele ou a depender de um store Mongo de terceiros pouco mantido. Conflita com o "MongoDB como banco principal".
- **JobRunr** se encaixa muito bem (Mongo nativo, dashboard, retries). O risco é o limite de cerca de 100 recorrentes no OSS, porque com 1 cron por produto e por cliente esse número é ultrapassado rápido. O Pro resolve, mas tem custo e roda num repositório privado. **[PENDENTE]**: estimar o número de produtos e schedules por ambiente.
- **@Scheduled + ShedLock** é o mais simples e gratuito, e já combina com o lock em Mongo com TTL do projeto. Por outro lado, não tem schedule dinâmico, retry nem dashboard prontos, então é preciso construí-los.

## Recomendação (para decisão do Michel) [INFERIDO]
1. **Padrão sugerido: um "tick" global com `@Scheduled` (por exemplo, a cada 1 minuto) + ShedLock no MongoDB**, que lê de uma coleção `varredura_schedules` (o cron de cada produto/tenant, mais `nextRunAt`) os produtos vencidos e publica cada execução no **Redis Streams**. Os workers das várias instâncias consomem a fila, com 3 retries e depois DLQ (o que já está previsto) e lock por produto no Mongo com TTL. O gatilho por tamanho de fila (500) publica no mesmo stream. O histórico fica numa coleção com índice TTL de cerca de 90 dias.
   - Vantagens: zero infra nova, sem custo de licença, sem limite de quantidade de schedules, e reaproveita o Redis Streams, a DLQ e o lock que já existem.
   - Custo: construir o cálculo de `nextRunAt` (o `CronExpression` do Spring serve) e uma tela ou endpoint de consulta.
2. **Alternativa: JobRunr OSS**, se o número de schedules por banco ficar comprovadamente abaixo de cerca de 100, ou **JobRunr Pro** se o dashboard e as filas por tenant valerem cerca de €850 por mês. **[PENDENTE]**: PoC com Boot 4.1.1 + Java 25 e confirmação comercial do preço.
3. **Quartz: não recomendado** neste stack, porque exige um banco relacional ou um store Mongo não oficial.

## Pendências
- [PENDENTE] Volume esperado de produtos/schedules por tenant e por ambiente.
- [PENDENTE] PoC do JobRunr 8.3+/9.x no Java 25 com Spring Boot 4.1.1 (a compatibilidade com Boot 4 está documentada; com Java 25 não foi verificada explicitamente).
- [PENDENTE] Se o dashboard é requisito (é o que mais pesa a favor do JobRunr).

## Fontes
- JobRunr v8.3 com Spring Boot 4: https://www.jobrunr.io/en/blog/jobrunr-v8.3/
- Instalação do JobRunr Pro (starter Boot 4, 9.0.1): https://www.jobrunr.io/en/documentation/pro/installation/
- JobRunr com MongoDB: https://www.jobrunr.io/en/documentation/storage/mongodb/
- JobRunr: Redis removido na v8: https://www.jobrunr.io/en/documentation/storage/custom-storageprovider/
- Preços e diferenças OSS vs Pro do JobRunr: https://www.jobrunr.io/en/pricing/
- FAQ do JobRunr (limite de 100 recorrentes, concorrência): https://www.jobrunr.io/en/blog/most-asked-questions/
- Licença do JobRunr Pro (cluster): https://www.jobrunr.io/en/understanding-your-license/
- Spring Boot com Quartz: https://docs.spring.io/spring-boot/reference/io/quartz.html
- QuartzJdbcProperties (Boot 4.1.1): https://docs.spring.io/spring-boot/api/java/org/springframework/boot/quartz/autoconfigure/QuartzJdbcProperties.html
- Quartz 2.5.2: https://github.com/quartz-scheduler/quartz/releases/tag/v2.5.2
- Licença do Quartz: https://www.quartz-scheduler.org/overview/license.html
- quartz-mongodb (terceiros): https://github.com/boomerang-io/flow.lib.scheduling
- Issue do Spring Boot sobre Mongo/Quartz: https://github.com/spring-projects/spring-boot/issues/33547
- ShedLock (provedores e matriz de compatibilidade): https://github.com/lukas-krecan/shedlock
- Versões do ShedLock: https://mvnrepository.com/artifact/net.javacrumbs.shedlock/shedlock-spring
- Agendamento no Spring (TaskScheduler/CronTrigger): https://docs.spring.io/spring-framework/reference/integration/scheduling.html
