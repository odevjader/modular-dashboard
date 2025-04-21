# Módulo: Gerador de Quesitos

Este documento detalha a funcionalidade, a API e o fluxo técnico do módulo "Gerador de Quesitos" do Modular Dashboard.

## Introdução

O objetivo deste módulo é auxiliar profissionais da área jurídica/previdenciária na elaboração de quesitos (perguntas) a serem respondidos por peritos judiciais em processos de concessão de benefícios (como auxílio-doença, aposentadoria por invalidez, BPC/LOAS). Ele utiliza Inteligência Artificial generativa para analisar documentos do caso e sugerir quesitos pertinentes.

## Funcionalidade Principal (Fluxo do Usuário)

1.  **Acesso:** O usuário navega até a seção "Gerador de Quesitos" na interface do dashboard.
2.  **Upload de Documentos:** O usuário seleciona e faz upload de um ou mais arquivos PDF relevantes para o caso (ex: petição inicial, laudos médicos, exames, documentos pessoais). O sistema previne o upload de arquivos duplicados na mesma sessão.
3.  **Seleção de Parâmetros:** O usuário seleciona o tipo de benefício previdenciário pretendido e a profissão/atividade habitual do requerente em listas pré-definidas (dropdowns).
4.  **(Opcional) Seleção de Modelo IA:** O usuário pode ter a opção de escolher um modelo de IA específico (ex: Gemini Pro, Gemma) para a geração.
5.  **Geração:** O usuário clica no botão "Gerar Quesitos".
6.  **Feedback Visual:** Durante o processamento (que pode levar algum tempo devido ao processamento dos PDFs e chamada à IA), a interface desabilita os inputs, exibe indicadores de carregamento e possivelmente mensagens de status (ex: "Processando PDF 1 de 3...", "Consultando IA...", frases aleatórias).
7.  **Exibição do Resultado:** Após a conclusão, os quesitos gerados pela IA são exibidos em uma área de texto na interface para o usuário revisar, copiar ou salvar.
8.  **Persistência de Estado (UI):** O último resultado gerado ou erro ocorrido é persistido no estado do frontend (usando Zustand) para que o usuário não perca a informação caso navegue para outra página e retorne durante ou após o processamento.

## Endpoint da API

O frontend interage com o seguinte endpoint no backend:

* **Método:** `POST`
* **Rota:** `/api/gerador_quesitos/v1/gerar`
* **Descrição:** Recebe os arquivos PDF e os parâmetros do formulário, processa os documentos, interage com o modelo de IA selecionado e retorna os quesitos gerados.
* **Autenticação:** (A ser definido/implementado - atualmente pode estar desprotegido ou dependerá do módulo Auth)
* **Request Body (multipart/form-data):**
    * `files`: Lista de `UploadFile` (Arquivos PDF enviados pelo usuário).
    * `tipo_beneficio`: `str` (Valor selecionado no formulário).
    * `profissao`: `str` (Valor selecionado no formulário).
    * `(opcional) model_name`: `str` (Identificador do modelo IA a ser usado, ex: "gemini-pro").
* **Response (Sucesso - HTTP 200):**
    ```json
    {
      "quesitos": "1. Quesito gerado pela IA...\n2. Outro quesito gerado..."
    }
    ```
* **Response (Erro):**
    * `HTTP 400 Bad Request`: Erro na validação dos dados de entrada (ex: nenhum arquivo enviado, parâmetro faltando).
    * `HTTP 422 Unprocessable Entity`: Erro na validação de tipos de dados (gerenciado pelo FastAPI/Pydantic).
    * `HTTP 500 Internal Server Error`: Erro inesperado durante o processamento de PDF, chamada à API da IA, ou outra falha interna. O corpo da resposta pode conter detalhes do erro.

## Fluxo Técnico (Backend)

Quando o endpoint `/api/gerador_quesitos/v1/gerar` é chamado, o backend executa os seguintes passos:

1.  **Recebimento e Validação:** O FastAPI recebe a requisição `multipart/form-data`. Os parâmetros do formulário (`tipo_beneficio`, `profissao`, `model_name`) e os arquivos (`files`) são validados usando Pydantic Schemas definidos em `backend/app/modules/gerador_quesitos/v1/schemas.py`.
2.  **Processamento de PDFs:**
    * O sistema itera sobre a lista de `UploadFile` recebida.
    * Para cada arquivo, utiliza a biblioteca `DoclingLoader` (integrada via `langchain-docling`) para carregar e extrair o conteúdo textual.
    * `DoclingLoader` é configurado para usar OCR (via Tesseract, que precisa estar instalado no ambiente/container) para extrair texto de imagens dentro dos PDFs, se houver.
    * O texto extraído de todos os PDFs válidos é concatenado em um único grande bloco de texto (contexto do caso).
    * *(**Nota:** Esta etapa é identificada como um potencial gargalo de performance).*
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

* **Backend:** FastAPI, Pydantic, Langchain, `langchain-google-genai`, `langchain-docling` (requer Tesseract OCR).
* **Frontend:** React, `Workspace` API, Zustand (para persistência de estado do resultado/erro).

## Considerações e Melhorias Futuras

* **Performance do PDF/OCR:** O processamento de múltiplos PDFs, especialmente com OCR, pode ser lento e consumir muitos recursos. Investigar otimizações no `DoclingLoader`, pré-processamento, ou mover essa tarefa para um background worker assíncrono (ex: Celery, ARQ) para não bloquear a resposta HTTP.
* **Caching:** Implementar cache (ex: Redis) para resultados de processamento de PDF ou talvez até para respostas da IA baseadas em contextos similares (requer análise cuidadosa).
* **Streaming de Resposta:** Para longas gerações de texto pela IA, considerar o uso de streaming para exibir os resultados progressivamente na UI.
* **Error Handling:** Refinar o tratamento de erros específicos da API da IA ou do processamento de arquivos.
* **UI/UX:** Melhorar o feedback visual durante o processamento e a apresentação dos resultados.