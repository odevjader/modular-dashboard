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
* **Request Body (`multipart/form-data`):**
    * `files`: Uma ou mais partes do formulário, cada uma contendo um arquivo PDF (`UploadFile`).
    * `tipo_beneficio`: Uma parte do formulário contendo o valor string (ex: `"Auxílio-Doença"`).
    * `profissao`: Uma parte do formulário contendo o valor string (ex: `"Motorista"`).
    * `(opcional) model_name`: Uma parte do formulário contendo o valor string (ex: `"gemini-pro"`).

* **Exemplo de Requisição (Conceitual):**
    * Uma requisição `POST` para `/api/gerador_quesitos/v1/gerar` com o `Content-Type: multipart/form-data`. A requisição conteria:
        * Uma ou mais partes chamadas `files`, cada uma com os dados binários de um arquivo PDF e seu nome/tipo.
        * Uma parte chamada `tipo_beneficio` com o valor texto selecionado.
        * Uma parte chamada `profissao` com o valor texto selecionado.
        * Opcionalmente, uma parte `model_name` com o nome do modelo.
    * Ferramentas como Postman ou código frontend (usando `FormData` com `Workspace`) podem construir essa requisição.

* **Exemplo de Resposta (Sucesso - HTTP 200):**
    ```json
    {
      "quesitos": "1. Considerando a atividade habitual de Motorista, quais limitações funcionais apresentadas nos laudos médicos de fls. XX-YY impedem o exercício desta profissão?\n2. O quadro descrito no exame de imagem de fls. ZZ é compatível com o exercício da atividade de Motorista de forma contínua?\n3. ..."
    }
    ```

* **Exemplo de Resposta (Erro de Validação - HTTP 422):** (Exemplo: `tipo_beneficio` não enviado)
    ```json
    {
      "detail": [
        {
          "loc": [
            "body",
            "tipo_beneficio"
          ],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```
* **Outras Respostas de Erro:**
    * `HTTP 400 Bad Request`: Pode ocorrer se nenhum arquivo for enviado ou outra validação customizada falhar.
    * `HTTP 500 Internal Server Error`: Para erros inesperados no processamento (PDF, OCR, IA).

## Fluxo Técnico (Backend)

Quando o endpoint `/api/gerador_quesitos/v1/gerar` é chamado, o backend executa os seguintes passos:

1.  **Recebimento e Validação:** O FastAPI recebe a requisição `multipart/form-data`. Os parâmetros do formulário (`tipo_beneficio`, `profissao`, `model_name`) e os arquivos (`files`) são validados usando Pydantic Schemas definidos em `backend/app/modules/gerador_quesitos/v1/schemas.py`.
2.  **Processamento de PDFs:**
    * O sistema itera sobre a lista de `UploadFile` recebida.
    * Para cada arquivo, utiliza a biblioteca `DoclingLoader` (integrada via `langchain-docling`) para carregar e extrair o conteúdo textual.
    * `DoclingLoader` é configurado para usar OCR (via Tesseract, **cuja instalação/acesso precisa ser garantida e documentada - ver `docs/02_SETUP_DESENVOLVIMENTO.md`**) para extrair texto de imagens dentro dos PDFs, se houver.
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