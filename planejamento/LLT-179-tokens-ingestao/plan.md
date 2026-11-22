# Plano — LLT-179

## Core (`lhamalog-core`, Core #8)

- Pacote `src/main/java/br/com/lhamalog/core/ingestiontoken/`, em camadas: `api` (`IngestionTokenController`, `TokenResponses`), `application` (`IngestionTokenService`, `TokenSecrets`, portas) e `infrastructure` (documentos e adaptadores do Mongo).
- Rotas em `/api/products/{productId}/tokens`: listar, gerar, `/{tokenId}/revoke`, `/{tokenId}/rotate` e `/audit`.
- Testes: `TokenSecretsTest`, `IngestionTokenServiceTest`, `MongoIngestionTokenRepositoryIntegrationTest` e `IngestionTokenControllerIntegrationTest`.

## Web (`lhamalog-web`, Web #15)

- `src/features/products/tokenContract.ts`: leitura das respostas do Core (`readTokenList`, `activeToken`, `readCreatedToken`, `readRotation`) e textos da tela.
- `src/features/products/otelSnippet.ts`: monta o exemplo de configuração, sempre com o valor de exemplo no lugar da chave.
- `src/features/products/components/`: `OtelConnectionCard.tsx`, `ApiKeyField.tsx`, `ConnectionStatusPanel.tsx`, `CopyButton.tsx` e `LogLevelSlider.tsx`.
- `src/shared/config.ts`, `infra/nginx/render-config.sh`, `compose.yaml`, `compose.dev.yaml`, `.env.example` e `README.md`: `VITE_OTLP_ENDPOINT`.
- Testes: `tests/ingestion-tokens.test.mjs`, `tests/otel-snippet.test.mjs` e `tests/public-config.test.mjs`. Os testes usam só o valor falso `llt_teste`.

## Ordem de merge no Web

**#12 (LLT-178) → #13 (LLT-123) → #14 (LLT-177) → #15 (LLT-179).** A #15 sai da branch da LLT-177.

## Validação

- **Core:** `mvnw clean verify` em 18/11/2026: 339 testes, 0 falhas, 0 pulados.
- **Web:** `npm test` e `npm run build`. A tela e a ausência da chave no armazenamento ficam no roteiro manual do `quickstart.md` do Web (T011).
