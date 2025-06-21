---
id: TASK-050
title: "DEV (Fase 2): Implementar Lógica de Extração de Texto no `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: done
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Implementar a funcionalidade principal de extração de texto de arquivos PDF dentro do `pdf_processor_service`. Isso pode envolver o uso de bibliotecas como PyMuPDF, pdfminer.six, etc. O texto extraído deve ser dividido em chunks apropriados para armazenamento e futuro processamento/embedding.

### Critérios de Aceitação

- [x] Função ou classe de serviço implementada para receber um caminho de arquivo PDF ou bytes de PDF.
- [x] Lógica para abrir e ler o PDF implementada.
- [x] Texto é extraído com sucesso de PDFs simples.
- [x] Texto extraído é dividido em chunks de tamanho gerenciável (e.g., por parágrafos, ou contagem de tokens/palavras).
- [x] Lógica para armazenar os chunks na tabela `pdf_processed_chunks` (criada na TASK-048) utilizando o `document_id` apropriado.

### Arquivos Relevantes

* `backend/pdf_processor_service/app/services/extraction_service.py`
* `backend/pdf_processor_service/app/services/document_service.py`
* `backend/pdf_processor_service/app/models/document.py`
* `backend/pdf_processor_service/requirements.txt`

### Relatório de Execução
### Relatório de Execução

1.  **Dependências**:
    *   Adicionado `pypdfium2` ao `backend/pdf_processor_service/requirements.txt` para manipulação e extração de texto de PDFs.
    *   Configurado SQLAlchemy models locais (`Document`, `DocumentChunk`) e gerenciamento de sessão de banco de dados no Passo de Preparação anterior (TASK-049 follow-up / TASK-050 pre-requisite subtask).

2.  **Serviço de Extração (`app/services/extraction_service.py`)**:
    *   `generate_file_hash(file_bytes: bytes) -> str`: Implementada para criar um hash SHA256 do conteúdo do arquivo.
    *   `extract_text_from_pdf(pdf_bytes: bytes) -> str`: Implementada usando `pypdfium2` para extrair o texto completo de um arquivo PDF fornecido como bytes. As páginas de texto são concatenadas com um separador de nova linha dupla.
    *   `chunk_text_by_paragraph(text: str) -> list[str]`: Implementada para dividir o texto extraído em chunks, usando parágrafos (delimitados por duas novas linhas) como base para a divisão.

3.  **Serviço de Documentos (`app/services/document_service.py`)**:
    *   `create_document_and_chunks(db: Session, file_contents: bytes, original_file_name: str | None = None) -> models.Document`:
        *   Orquestra o processo de processamento de um PDF.
        *   Gera um hash do conteúdo do arquivo.
        *   Verifica se um `Document` com o mesmo hash já existe no banco de dados.
        *   Se não existir, cria um novo registro `Document`.
        *   Se existir, remove os `DocumentChunk`s antigos associados a ele e atualiza metadados (como `file_name`) se necessário, implementando uma estratégia de sobrescrita simples.
        *   Utiliza `extraction_service` para extrair texto e dividi-lo em chunks.
        *   Salva cada chunk de texto como um registro `DocumentChunk` associado ao `Document`.
        *   Persiste todas as alterações no banco de dados.

4.  **Exportação de Serviço (`app/services/__init__.py`)**:
    *   Criado para exportar a função `create_document_and_chunks`, tornando-a facilmente acessível para os futuros endpoints da API.

Esta implementação cobre a lógica central para processar PDFs, extrair seu texto, dividi-lo em partes e persistir essa informação no banco de dados do serviço.
