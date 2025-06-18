---
id: TASK-026
title: "DEV: Construir Orquestrador de Respostas com LLM (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-023", "TASK-019"] # Depende da busca vetorial e da doc do LLM client
assignee: Jules
---

### Descrição

Criar `src/query_processor.py` em `transcritor-pdf` usando busca vetorial e `llm_client.py`. (Original TASK-009 do backlog)

### Critérios de Aceitação

- [ ] Arquivo `transcritor-pdf/src/query_processor.py` criado.
- [ ] Classe/função que recebe pergunta e ID de documento.
- [ ] Utiliza a busca vetorial (TASK-023) para obter contexto.
- [ ] Constrói prompt para LLM e chama `llm_client.py`.
- [ ] Retorna resposta do LLM.

### Arquivos Relevantes

* `transcritor-pdf/src/query_processor.py`
* `transcritor-pdf/src/extractor/llm_client.py`

### Relatório de Execução

- Criado o novo arquivo `transcritor-pdf/src/query_processor.py`.
- Implementada a função assíncrona `async def get_llm_answer_with_context(user_query: str, document_filename: Optional[str] = None, top_k_context_chunks: int = 3) -> Dict[str, Any]` dentro deste arquivo.
- A função realiza a seguinte lógica de orquestração:
    1.  Chama `vector_store_handler.search_similar_chunks()` para buscar chunks de texto relevantes (contexto) com base na `user_query` e, opcionalmente, no `document_filename`. O número de chunks é determinado por `top_k_context_chunks`.
    2.  Formata o texto dos chunks recuperados em uma única string de contexto.
    3.  Constrói um prompt para o LLM utilizando `SystemMessage` (para definir o comportamento do assistente) e `HumanMessage` (contendo o contexto formatado e a `user_query`). O prompt instrui o LLM a responder em português e a indicar se o contexto é insuficiente.
    4.  Obtém uma instância do cliente LLM através de `llm_client.get_llm_client()`.
    5.  Chama o método `llm.invoke(messages)` para obter a resposta do LLM.
    6.  Retorna um dicionário contendo a resposta do LLM (`answer`), os chunks de contexto recuperados (`retrieved_context`), e uma mensagem de erro (`error`) se alguma falha crítica ocorrer.
- Adicionado tratamento de exceções para falhas durante a busca de contexto e a chamada ao LLM.
- Importações necessárias, incluindo `SystemMessage` e `HumanMessage` de `langchain_core.messages`, foram adicionadas.
- Todos os critérios de aceitação foram atendidos: o arquivo foi criado, a função recebe a pergunta e opcionalmente o ID do documento, utiliza a busca vetorial, constrói o prompt, chama o LLM e retorna a resposta.
