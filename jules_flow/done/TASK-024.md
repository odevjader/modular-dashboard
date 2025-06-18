---
id: TASK-024
title: "TEST-PLAN: Planejar Testes para Busca Vetorial (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-023"]
assignee: Jules
---

### Descrição

Testes unitários para a função de busca vetorial: mockar DB/dados, verificar query SQL, verificar resultados.

### Critérios de Aceitação

- [ ] Plano de teste criado (e.g., `docs/tests/vector_search_test_plan.md`).
- [ ] Detalha como mockar a DB e os dados vetoriais.
- [ ] Especifica asserções para a query SQL gerada e para os resultados.

### Arquivos Relevantes

* `docs/tests/vector_search_test_plan.md`

### Relatório de Execução

- Analisado o comportamento da função `search_similar_chunks` em `transcritor-pdf/src/vectorizer/vector_store_handler.py`.
- Definidos cenários de teste unitário detalhados, cobrindo:
    - Busca bem-sucedida com e sem filtro de nome de arquivo.
    - Cenário sem resultados encontrados.
    - Validação de entrada para `top_k`.
    - Erros na geração de embedding da query.
    - Erros de conexão com o banco de dados e na execução da query.
    - Tratamento de metadados malformados retornados do banco de dados.
    - Falha por configuração de banco de dados ausente.
- Delineada a estratégia de mocking para dependências como `embedding_generator.embed_query`, `asyncpg.connect`, e métodos do objeto de conexão `asyncpg.Connection` (e.g., `fetch`).
- Estruturado o plano de teste com seções padrão: Introdução, Ambiente de Teste (unitário), Estratégia de Mocking, Casos de Teste detalhados, Critérios de Sucesso e Itens Fora do Escopo.
- Criado o documento do plano de teste unitário em `docs/tests/vector_search_test_plan.md`.
- Todos os critérios de aceitação foram atendidos: o plano de teste detalha o mocking e especifica as asserções necessárias.
