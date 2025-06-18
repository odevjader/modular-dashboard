---
id: TASK-028
title: "TEST-IMPL: Implementar Testes para Orquestrador de Respostas (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-027"]
assignee: Jules
---

### Descrição

Implementar os testes unitários para o orquestrador de respostas.

### Critérios de Aceitação

- [ ] Testes unitários implementados em `transcritor-pdf/tests/test_query_processor.py` (a ser criado).
- [ ] Mocks para busca vetorial e LLM client utilizados.
- [ ] Asserções verificam o prompt e o processamento da resposta.

### Arquivos Relevantes

* `transcritor-pdf/tests/test_query_processor.py`

### Relatório de Execução

- Criado o arquivo de teste `transcritor-pdf/tests/test_query_processor.py`.
- Implementados testes unitários para a função `get_llm_answer_with_context` (localizada em `src.query_processor.py`) conforme o plano de teste de TASK-027 (`docs/tests/query_processor_test_plan.md`).
- Os seguintes cenários de teste foram implementados (TC_QP_001 a TC_QP_007):
    - **TC_QP_001**: Consulta bem-sucedida com contexto encontrado, verificando a chamada à busca vetorial, a construção do prompt (System e Human messages), a chamada ao LLM e a estrutura da resposta.
    - **TC_QP_002**: Consulta onde nenhum contexto é encontrado pela busca vetorial, verificando se o prompt reflete a ausência de contexto e a resposta do LLM é processada.
    - **TC_QP_003**: Falha durante a recuperação de contexto (e.g., `ConnectionError` da busca vetorial), verificando se o LLM não é chamado e uma mensagem de erro apropriada é retornada.
    - **TC_QP_004**: Falha durante a chamada ao LLM (`llm.invoke()` lança exceção), verificando o tratamento de erro.
    - **TC_QP_005**: Falha durante a inicialização do cliente LLM (`get_llm_client()` lança `ValueError`), verificando o tratamento de erro.
    - **TC_QP_006**: Resposta malformada do LLM (sem atributo `content`), verificando o tratamento de erro.
    - **TC_QP_007**: Tratamento de chunks de contexto com `text_content` vazio ou ausente, garantindo que o prompt seja construído corretamente.
- Utilizado `unittest.mock` (`patch`, `MagicMock`, `AsyncMock`) para mockar as dependências:
    - `vector_store_handler.search_similar_chunks` (como `AsyncMock`).
    - `llm_client.get_llm_client` e o método `invoke` do cliente LLM mockado.
    - O logger (`caplog` do pytest) para verificar mensagens de log importantes.
- Asserções foram implementadas para verificar:
    - Argumentos passados aos mocks (especialmente a formatação do prompt para o LLM).
    - Valores de retorno da função `get_llm_answer_with_context`.
    - Propagação ou tratamento de exceções.
    - Mensagens de log específicas.
- Todos os testes foram definidos como `async def` e utilizam `await` para interagir com a função assíncrona testada, sendo compatíveis com `pytest` (usando `pytest.mark.asyncio`).
- Os critérios de aceitação foram atendidos: testes unitários implementados no arquivo especificado, mocks utilizados para dependências externas, e asserções verificam a lógica de construção do prompt e o processamento da resposta.
