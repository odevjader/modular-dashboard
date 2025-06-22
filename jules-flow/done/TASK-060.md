---
id: TASK-060
title: "TEST-IMPL (Fase 4 Piloto): Implementar Testes para `gerador_quesitos` Refatorado"
epic: "Fase 4: Módulo Piloto e Integração"
status: done
priority: medium
dependencies: ["TASK-059"]
assignee: Jules
---

### Descrição

Implementar os testes de componente, integração e E2E (conforme viável) para o módulo `gerador_quesitos` refatorado, conforme definido no plano de teste da `TASK-059`.

### Critérios de Aceitação

- [x] Testes para o frontend do `gerador_quesitos` implementados.
- [x] Testes para o backend do `gerador_quesitos` implementados.
- [x] Testes E2E (se aplicável) para o fluxo completo do `gerador_quesitos` refatorado implementados. (Decidido por realizar manualmente com base nos cenários GQ-E2E do plano de teste)
- [ ] Todos os testes passando em ambiente de desenvolvimento/CI. (Execução manual pendente pelo usuário)

### Arquivos Relevantes

* `frontend/src/modules/gerador_quesitos/GeradorQuesitos.tsx`
* `frontend/src/modules/gerador_quesitos/tests/GeradorQuesitos.test.tsx`
* `backend/app/modules/gerador_quesitos/v1/endpoints.py`
* `backend/app/modules/gerador_quesitos/tests/v1/test_endpoints_gerador_quesitos.py`
* `docs/tests/gerador_quesitos_refatorado_test_plan.md` (referência para os testes)

### Relatório de Execução

**Testes de Frontend (Componente):**
- Implementados utilizando Jest e React Testing Library.
- Arquivo de teste: `frontend/src/modules/gerador_quesitos/tests/GeradorQuesitos.test.tsx`.
- Componente modificado: `frontend/src/modules/gerador_quesitos/GeradorQuesitos.tsx` (adicionado `data-testid` para o input de arquivo).
- Cobertura dos casos de teste GQ-FE-001 a GQ-FE-006 do plano de teste, adaptados para a estrutura atual do componente e store (Zustand).
- Foco em:
    - Renderização inicial e elementos principais.
    - Seleção de benefício e profissão.
    - Upload de arquivo PDF válido e tratamento de tipo de arquivo inválido.
    - Exibição de nome de arquivo selecionado e remoção de arquivo.
    - Simulação de chamadas à action do store (`uploadAndProcessSinglePdfForQuesitos`).
    - Verificação de estados de loading (com `CircularProgress` e feedback visual).
    - Exibição de resultados de quesitos e mensagens de erro do store.
    - Lógica de limpeza de resultados (implícita na nova submissão ou remoção de arquivo).
- A execução dos testes foi pulada e será realizada manualmente pelo usuário.

**Testes de Backend (API/Integração):**
- Implementados utilizando Pytest e TestClient do FastAPI.
- Arquivo de teste: `backend/app/modules/gerador_quesitos/tests/v1/test_endpoints_gerador_quesitos.py`.
- Endpoint modificado: `backend/app/modules/gerador_quesitos/v1/endpoints.py` (ajustes na lógica de instanciação do LLM para considerar a temperatura e outros casos).
- Cobertura dos casos de teste GQ-BE-001 a GQ-BE-006 do plano de teste para o endpoint `/gerar_com_referencia_documento`.
- Testes adicionados/modificados para cobrir:
    - Geração de quesitos com sucesso usando `document_id`, benefício, profissão, modelo e temperatura.
    - Tratamento de `document_id` inexistente.
    - Tratamento de texto de documento vazio/inadequado.
    - Validação de payload (ausência de `document_id`, `beneficio`, `profissao`).
    - Simulação de erro interno no LLM.
    - Comportamento quando a API key do Google está ausente (para modelo padrão e específico).
    - Comportamento quando o template de prompt não é carregado.
    - Teste para o endpoint legado `/gerar` (que está desativado e retorna mensagem específica).
- A execução dos testes foi pulada e será realizada manualmente pelo usuário.

**Testes End-to-End (E2E):**
- Decidiu-se por não implementar testes E2E automatizados com Cypress/Playwright nesta etapa, visando simplicidade e devido à complexidade de configuração no ambiente atual.
- Os cenários GQ-E2E-001, GQ-E2E-002 e GQ-E2E-003 detalhados em `docs/tests/gerador_quesitos_refatorado_test_plan.md` servem como guia para testes manuais E2E, que serão realizados pelo usuário.

**Observação Geral:**
A execução de todos os testes (frontend e backend) foi postergada para ser realizada manualmente pelo usuário, conforme solicitado. Portanto, o critério de aceitação "Todos os testes passando em ambiente de desenvolvimento/CI" está pendente dessa validação manual.
