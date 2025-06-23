# docs/modules/01_GERADOR_QUESITOS.md
# Módulo: Gerador de Quesitos

Este documento detalha a funcionalidade, a API e o fluxo técnico do módulo "Gerador de Quesitos" do Modular Dashboard.

## Introdução

O objetivo deste módulo é auxiliar profissionais da área jurídica/previdenciária na elaboração de quesitos (perguntas) a serem respondidos por peritos judiciais em processos de concessão de benefícios (como auxílio-doença, aposentadoria por invalidez, BPC/LOAS). Ele utiliza Inteligência Artificial generativa para analisar documentos do caso e sugerir quesitos pertinentes.

## Funcionalidade Principal (Fluxo do Usuário)

1.  **Acesso:** O usuário navega até a seção "Gerador de Quesitos" na interface do dashboard.
2.  **Upload de Documentos:** O usuário seleciona e faz upload de um ou mais arquivos PDF relevantes para o caso (ex: petição inicial, laudos médicos, exames, documentos pessoais). O sistema evita o upload de arquivos duplicados na mesma sessão.
3.  **Seleção de Parâmetros:** O usuário seleciona o tipo de benefício previdenciário pretendido e a profissão/atividade habitual do requerente em listas pré-definidas (dropdowns).
4.  **(Opcional) Seleção de Modelo IA:** Opcionalmente, o usuário pode escolher um modelo de IA específico (ex: Gemini Pro, Gemma) para a geração.
5.  **Geração:** O usuário clica no botão "Gerar Quesitos".
6.  **Feedback Visual:** Durante o processamento (que pode levar algum tempo devido ao processamento dos PDFs e chamada à IA), a interface desabilita os inputs, exibe indicadores de carregamento e possivelmente mensagens de status (ex: "Processando PDF 1 de 3...", "Consultando IA...").
7.  **Exibição do Resultado:** Após a conclusão, os quesitos gerados pela IA são exibidos em uma área de texto na interface para o usuário revisar, copiar ou salvar.
8.  **Persistência de Estado (UI):** O último resultado gerado ou erro ocorrido é persistido no estado do frontend (usando Zustand) para que o usuário não perca a informação caso navegue para outra página e retorne durante ou após o processamento.

## Endpoints da API

O módulo `gerador_quesitos` expõe o seguinte endpoint principal:

### Gerar Quesitos com Referência de Documento

*   **Método:** `POST`
*   **Rota:** `/api/gerador_quesitos/v1/gerar_com_referencia_documento`
*   **Descrição:** Recebe o nome de um arquivo de documento (previamente processado pelo serviço `transcritor-pdf`), informações do caso (benefício, profissão) e o nome do modelo de IA. Busca o conteúdo textual do documento no banco de dados, formata um prompt e chama o modelo de IA para gerar os quesitos.
*   **Autenticação:** (A ser definido/implementado - atualmente pode estar desprotegido ou dependerá do módulo Auth).
*   **Request Body (JSON):**
    ```json
    {
      "document_filename": "nome_do_arquivo.pdf",
      "beneficio": "Auxílio-Doença",
      "profissao": "Motorista",
      "modelo_nome": "gemini-pro" // ou "<Modelo Padrão>"
    }
    ```
    *   `document_filename`: String, nome do arquivo do documento como armazenado pelo `transcritor-pdf`.
    *   `beneficio`: String, tipo de benefício previdenciário.
    *   `profissao`: String, profissão do requerente.
    *   `modelo_nome`: String, nome do modelo de IA ou `"<Modelo Padrão>"`.
*   **Exemplo de Resposta (Sucesso - HTTP 200):**
    ```json
    {
      "quesitos_texto": "1. Considerando a atividade habitual de Motorista, quais limitações funcionais apresentadas nos laudos médicos de fls. XX-YY impedem o exercício desta profissão?\n2. ..."
    }
    ```
*   **Respostas de Erro Comuns:**
    *   `HTTP 404 Not Found`: Se o `document_filename` não for encontrado no banco de dados ou não tiver conteúdo processado.
    *   `HTTP 422 Unprocessable Entity`: Se os dados do payload forem inválidos.
    *   `HTTP 500 Internal Server Error`: Para erros na consulta ao banco, falha na comunicação com a IA, ou outros erros inesperados.
    *   `HTTP 503 Service Unavailable`: Se o serviço de IA não estiver configurado ou disponível.

**(Nota: O endpoint anterior `/api/gerador_quesitos/v1/gerar` que realizava upload direto de PDFs foi descontinuado e removido em favor deste fluxo que utiliza documentos pré-processados pelo serviço `transcritor-pdf`.)**

## Fluxo Técnico (Backend)

Quando o endpoint `/api/gerador_quesitos/v1/gerar_com_referencia_documento` é chamado:

1.  **Recebimento e Validação:** O FastAPI recebe o payload JSON e o valida usando o schema Pydantic `GerarQuesitosComDocIdPayload`.
2.  **Busca do Conteúdo do Documento:**
    *   O sistema consulta a tabela `documents` (populada pelo `transcritor-pdf`) usando o `document_filename` fornecido.
    *   Os chunks de texto (`text_content`) associados ao arquivo são recuperados e concatenados para formar o contexto completo do documento.
3.  **Construção do Prompt para LLM:**
    * Um prompt template estruturado é preenchido com:
        * O contexto extraído dos PDFs.
        * O tipo de benefício e a profissão informados pelo usuário.
        * Instruções claras para a IA gerar quesitos periciais relevantes para aquele contexto e tipo de caso.
4.  **Interação com LLM (Langchain):**
    * Utiliza-se a integração `langchain-google-genai` para instanciar um cliente para o modelo de IA selecionado (ex: `ChatGoogleGenerativeAI`).
    * O prompt construído é enviado para a API do Google AI (Gemini/Gemma) através do Langchain.
    * O sistema aguarda a resposta da IA. Mecanismos de retentativa (como a biblioteca `tenacity`) podem ser usados para lidar com falhas transitórias na API externa.
5.  **Formatação e Retorno:**
    * A resposta (texto dos quesitos) recebida da IA é extraída.
    * A resposta é formatada no schema Pydantic de saída (`{"quesitos": "..."}`) e retornada ao frontend com status HTTP 200.
    * Em caso de erro em qualquer etapa, uma exceção HTTP apropriada (4xx ou 5xx) é levantada e retornada.

## Tecnologias Específicas do Módulo

* **Backend:** FastAPI, Pydantic, Langchain, `langchain-google-genai`. A dependência direta de `langchain-docling` e Tesseract OCR neste módulo foi removida em favor da integração com o serviço `transcritor-pdf`.
* **Frontend:** React, API `fetch` (com `FormData`), Zustand (para persistência de estado do resultado/erro).

## Considerações e Melhorias Futuras

* **Integração com Transcritor-PDF:** Fortalecer a integração com o serviço `transcritor-pdf` para consumir os documentos processados. Atualmente, o endpoint `/gerar_com_referencia_documento` busca chunks diretamente do banco de dados que é populado pelo `transcritor-pdf`.
* **Caching:** Implementar cache (ex: Redis) para respostas da IA baseadas em contextos similares.
* **Streaming de Resposta:** Para longas gerações de texto pela IA, considerar o uso de streaming para exibir os resultados progressivamente na UI.
* **Error Handling:** Refinar o tratamento de erros específicos da API da IA ou do processamento de arquivos.
* **UI/UX:** Melhorar o feedback visual durante o processamento e a apresentação dos resultados.