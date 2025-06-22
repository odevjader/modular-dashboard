---
id: TASK-058
title: "DEV (Fase 4 Piloto): Refatorar Backend do `gerador_quesitos` para Usar Texto Pré-processado"
epic: "Fase 4: Módulo Piloto e Integração"
status: done
priority: medium
dependencies: ["TASK-050"]
assignee: Jules
---

### Descrição

Modificar o endpoint backend do módulo `gerador_quesitos` (`backend/app/modules/gerador_quesitos/`) para não processar mais o arquivo PDF diretamente. Em vez disso, deve receber um `document_id` (ou `file_hash`/`task_id` correspondente a um documento já processado pela pipeline de documentos) e buscar o texto pré-processado (e possivelmente chunks/embeddings) do banco de dados para então executar sua lógica de geração de quesitos com LangChain.

### Critérios de Aceitação

- [x] Endpoint backend do `gerador_quesitos` modificado para aceitar um `document_id` (ou similar) em vez de um upload de arquivo direto.
- [x] Lógica implementada para buscar texto/chunks processados do banco de dados (e.g., da tabela `pdf_processed_chunks` ou similar) usando o `document_id`.
- [x] Lógica de geração de quesitos com LangChain adaptada para usar o texto recuperado do banco de dados.
- [x] Endpoint retorna os quesitos gerados.

### Arquivos Relevantes

* `backend/app/modules/gerador_quesitos/v1/endpoints.py`
* `backend/app/modules/gerador_quesitos/v1/esquemas.py`
* `backend/app/models/document.py` (as it's used for querying)

### Relatório de Execução
### Relatório de Execução

O backend do módulo `gerador_quesitos` foi refatorado para consumir texto pré-processado de documentos identificados por `document_id`, em vez de processar arquivos PDF diretamente.

1.  **Schema de Request (`esquemas.py`)**:
    *   Criado o Pydantic model `GerarQuesitosComDocIdPayload` para o corpo da requisição do novo endpoint. Este schema inclui `document_id: int`, `beneficio: str`, `profissao: str`, e `modelo_nome: str`.

2.  **Endpoint (`endpoints.py`)**:
    *   **Novo Endpoint**: Adicionado `POST /gerar_com_referencia_documento`.
        *   Aceita o payload `GerarQuesitosComDocIdPayload`.
        *   Utiliza `Depends(get_db)` para obter uma sessão de banco de dados.
    *   **Busca de Dados**: Implementada a lógica para consultar a tabela `document_chunks` (usando o model `DocumentChunk` de `app.models.document`) filtrando pelo `document_id` recebido, ordenando por `chunk_order`.
        *   Se nenhum chunk é encontrado, retorna HTTP 404.
        *   Os textos dos chunks são concatenados para reconstruir o conteúdo do documento.
    *   **Lógica LLM**:
        *   O código de inicialização e seleção do LLM (usando `ChatGoogleGenerativeAI`) foi reativado e adaptado.
        *   O sistema tenta usar um modelo LLM padrão (inicializado no startup do módulo, se `GOOGLE_API_KEY` estiver presente) ou um modelo especificado no payload.
        *   Tratamento de erro para falha na inicialização do LLM ou ausência da API key foi incluído.
        *   Se nenhum LLM estiver disponível, retorna uma resposta placeholder indicando a indisponibilidade.
        *   O prompt (carregado do arquivo `gerar_quesitos_prompt.txt`) é formatado com o texto recuperado do banco de dados e os outros dados do payload (`beneficio`, `profissao`).
        *   A chamada assíncrona ao LLM (`llm_to_use.ainvoke([message])`) foi reativada.
        *   A resposta do LLM é retornada no schema `RespostaQuesitos`.
        *   Tratamento de erro para falhas na chamada ao LLM foi incluído.
    *   **Endpoint Antigo**: O endpoint original `/gerar` (que aceitava `UploadFile`) foi mantido, mas sua lógica principal de processamento e chamada LLM permanece desativada, efetivamente o depreciando em favor do novo fluxo.
    *   **Autenticação**: O novo endpoint está preparado para ter autenticação (`Depends(get_current_active_user)`) mas está comentado por padrão, podendo ser ativado se necessário.

Esta refatoração alinha o backend do `gerador_quesitos` com a arquitetura de processamento de documentos centralizada, onde ele agora consome dados de documentos já processados pela pipeline (TASK-048 a TASK-053).
