---
id: TASK-027
title: "TEST-PLAN: Planejar Testes para Orquestrador de Respostas (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-026"]
assignee: Jules
---

### Descrição

Testes unitários para o orquestrador: mockar busca vetorial e cliente LLM, verificar construção do prompt, verificar processamento da resposta.

### Critérios de Aceitação

- [ ] Plano de teste criado (e.g., `docs/tests/query_processor_test_plan.md`).
- [ ] Detalha mocks para busca vetorial e LLM client.
- [ ] Especifica asserções para o prompt e a resposta.

### Arquivos Relevantes

* `docs/tests/query_processor_test_plan.md`

### Relatório de Execução

- Analisado o comportamento da função `get_llm_answer_with_context` em `transcritor-pdf/src/query_processor.py` e suas interações com `vector_store_handler.search_similar_chunks` e `llm_client.get_llm_client`.
- Definidos cenários de teste unitário detalhados para `get_llm_answer_with_context`, cobrindo:
    - Processamento bem-sucedido da query com contexto encontrado.
    - Query quando nenhum contexto é encontrado pela busca vetorial.
    - Falha na recuperação de contexto (erro de banco de dados).
    - Falha na chamada ao LLM.
    - Falha na inicialização do cliente LLM.
    - Tratamento de resposta malformada do LLM.
    - Tratamento de chunks de contexto com `text_content` vazio.
- Delineada a estratégia de mocking para as dependências:
    - `vector_store_handler.search_similar_chunks` (para controlar o contexto retornado ou simular erros).
    - `llm_client.get_llm_client()` (para retornar um mock do cliente LLM ou simular erros de inicialização).
    - Método `invoke()` do mock do cliente LLM (para controlar a resposta do LLM ou simular erros).
    - Logger para verificar mensagens de log.
- Especificadas asserções para verificar as chamadas aos mocks (incluindo argumentos como o prompt construído), o valor de retorno da função, e o tratamento de erros.
- Estruturado o plano de teste com seções padrão: Introdução, Ambiente de Teste (unitário), Estratégia de Mocking, Casos de Teste detalhados, Critérios de Sucesso e Itens Fora do Escopo.
- Criado o documento do plano de teste unitário em `docs/tests/query_processor_test_plan.md`.
- Todos os critérios de aceitação foram atendidos: o plano de teste detalha a estratégia de mocking e especifica as asserções para o prompt e a resposta.
