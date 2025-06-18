---
id: TASK-023
title: "DEV: Desenvolver Inteligência de Busca Vetorial (Transcritor-PDF)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-019", "TASK-020"] # Depende da doc do pgvector e do processamento de PDF que armazena os vetores
assignee: Jules
---

### Descrição

Em `transcritor-pdf/src/vectorizer/vector_store_handler.py`, implementar busca por similaridade em pgvector. (Original TASK-008 do backlog)

### Critérios de Aceitação

- [ ] Função em `vector_store_handler.py` aceita query e ID de documento.
- [ ] Conecta ao DB e executa query de similaridade vetorial (e.g., `<=>`) em `pgvector`.
- [ ] Retorna chunks de texto relevantes.

### Arquivos Relevantes

* `transcritor-pdf/src/vectorizer/vector_store_handler.py`

### Relatório de Execução

- Implementada a função `async def search_similar_chunks(query_text: str, top_k: int = 5, document_filename: Optional[str] = None) -> List[Dict[str, Any]]` no arquivo `transcritor-pdf/src/vectorizer/vector_store_handler.py`.
- A função realiza os seguintes passos:
    1. Gera um embedding vetorial para o `query_text` de entrada utilizando `embedding_generator.get_embedding_client().embed_query()`.
    2. Conecta-se ao banco de dados PostgreSQL utilizando `asyncpg` e as configurações carregadas por `load_db_config()`.
    3. Constrói dinamicamente uma query SQL para buscar por similaridade:
        - Utiliza o operador de distância cosseno `<=>` do `pgvector` para comparar o embedding da query com os embeddings armazenados na tabela `documents`.
        - Permite filtragem opcional por `document_filename` (acessando `metadata->>'filename'` dwellers).
        - Ordena os resultados pela distância (similaridade) e limita a quantidade por `top_k`.
    4. Executa a query e processa os resultados.
    5. Converte a distância cosseno (0 para idêntico, 2 para oposto) em um `similarity_score` (1 - distância) para facilitar a interpretação (maior é mais similar).
    6. Retorna uma lista de dicionários, cada um contendo `chunk_id`, `text_content`, `metadata` e `similarity_score`.
- Incluído tratamento de erros para a geração de embeddings e operações de banco de dados.
- Verificado que as importações necessárias estão presentes no arquivo.
- Os critérios de aceitação foram atendidos:
    - A função aceita uma query e opcionalmente um `document_filename`.
    - Conecta ao DB e executa a query de similaridade vetorial.
    - Retorna os chunks de texto relevantes com score de similaridade.
