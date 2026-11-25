# Dataset de logs — amostras (LhamaLog, v3)

Pasta criada em 19/10/2026 para a análise "Plano de Monetização v3 — Cobrança por uso".
Contém **amostras pequenas** dos datasets usados para medir bytes/log, compressão, tamanho OTLP e tamanho de índice no Elasticsearch. Os arquivos completos (≈ 2,6 GB, 18,16 milhões de linhas) ficaram apenas na box de trabalho (`/workspace/logs-dataset/data/`) e podem ser baixados de novo pelas fontes abaixo.

## Fonte e licença

- **Loghub** — coleção de logs de sistemas (LogPAI / CUHK).
  - GitHub: https://github.com/logpai/loghub
  - Zenodo (arquivos completos): https://zenodo.org/records/8196385 — DOI 10.5281/zenodo.8196385 — licença **CC BY 4.0** (exige atribuição).
  - O README do GitHub diz que os logs são "freely available for research or academic work". Para uso **comercial**, confirmar os termos antes; aqui o uso é acadêmico (projeto da faculdade).
  - Citação pedida pelos autores: Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics*. IEEE ISSRE, 2023.
- Datasets usados (12): Apache, BGL, HDFS (HDFS_v1), HPC, Hadoop, HealthApp, Linux, Mac, OpenStack, Proxifier, SSH, Zookeeper.
  - Hadoop: todos os arquivos de container concatenados; OpenStack: abnormal + normal1 + normal2 concatenados.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `<Dataset>_amostra_200.log` (12) | As 200 primeiras linhas de cada dataset, sem alteração |
| `HDFS_amostra_100_otlp.json`, `SSH_amostra_100_otlp.json` | 100 linhas convertidas para OTLP/JSON (`ExportLogsServiceRequest`). **traceId/spanId são sintéticos** (derivados de md5), e os atributos de recurso (`service.name`, `host.name`, `lhamalog.tenant.id`) são fictícios |
| `medicoes_datasets.csv` | Medições por dataset: linhas, bytes, bytes/log, gzip, zstd, OTLP |
| `measure.py` | Script de medição (gzip nível 6, zstd nível 3, em streaming; OTLP das 1.000 primeiras linhas, lotes de 100) |
| `es_index.py` | Script que indexa 20 mil linhas/dataset no Elasticsearch 8.15.3 local (3 mapeamentos) |
| `es_measure.json`, `es_vec.json`, `es_throughput.json` | Resultados: tamanho de índice, vetores 384 dims, vazão bulk |
| `latencia_box_amostras_novaconexao.txt`, `latencia_box_amostras_conexaoreutilizada.txt` | Amostras brutas de latência medidas da box (**só referência**: a box não está na localização do cliente) |

## Resultados principais (19/10/2026)

- Bytes/log bruto: **143,1** (média ponderada pelo volume) · 132,1 (média simples) · 121,2 (mediana)
- Logs por GB bruto: ≈ **6,99 milhões** (ponderado)
- Compressão (ponderada): gzip 10,9× · zstd 10,7× (média simples: gzip 14,0× · zstd 14,9×)
- OTLP JSON: ≈ 448 B/log (3,3× o texto bruto); OTLP JSON + zstd ≈ 0,32× o bruto
- Elasticsearch (1 shard, 0 réplica, após force-merge): mapeamento dinâmico 2,45× o bruto · otimizado (`match_only_text` + `best_compression`) **1,34×** · logsdb 1,85×

## Metodologia (resumo)

1. Download dos zips do Zenodo, extração e concatenação por dataset.
2. `measure.py`: conta linhas e bytes; comprime em streaming com gzip/zstd; converte 1.000 linhas para OTLP JSON.
3. `es_index.py`: Elasticsearch 8.15.3 single-node (heap 1 GB, segurança desligada), bulk, `_forcemerge` para 1 segmento, `_stats` → `store.size_in_bytes`.
4. Latência: `curl` 10 amostras/endpoint (conexão nova e reutilizada). A box sai por proxy (egress próximo à Costa Leste dos EUA), então os números **não** representam o cliente. No produto, o teste roda no navegador/collector do cliente (ver doc "Proposta - Teste de latência do provedor").
