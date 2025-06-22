---
id: TASK-062
title: "DEV (Fase 5): Configurar Logging Estruturado e Avaliar APM"
epic: "Fase 5: Governança e Maturidade"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Implementar um sistema de logging estruturado em todos os serviços backend (API Principal, `transcritor-pdf`, e o futuro `pdf_processor_service`). Avaliar e potencialmente integrar uma ferramenta de Application Performance Monitoring (APM) básica para observabilidade.

### Critérios de Aceitação

- [ ] Logging configurado para usar formato estruturado (e.g., JSON) em todos os serviços backend.
- [ ] Logs incluem informações relevantes como timestamp, nível de log, mensagem, e contexto da requisição (e.g., endpoint, user_id se aplicável).
- [ ] Logs são facilmente agregáveis e pesquisáveis (considerar output para stdout para coleta por Docker/K8s).
- [ ] Pesquisa sobre ferramentas APM (e.g., Sentry, Datadog, OpenTelemetry) realizada e uma recomendação documentada.
- [ ] (Opcional, dependendo da avaliação) Integração básica de uma ferramenta APM para monitorar performance de endpoints chave e rastrear erros.

### Arquivos Relevantes

* `backend/app/core/logging_config.py`
* `transcritor-pdf/src/logging_config.py`
* `pdf_processor_service/app/logging_config.py`
* `docs/reference/apm_evaluation.md`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
