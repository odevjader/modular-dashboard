# Plano de Teste: Módulo `gerador_quesitos` Refatorado

**ID da Tarefa:** TASK-059
**Épico:** Fase 4: Módulo Piloto e Integração
**Dependências:** TASK-058 (Refatoração do `gerador_quesitos`)

## 1. Visão Geral

Este plano de teste detalha os procedimentos para verificar a funcionalidade do módulo `gerador_quesitos` após sua refatoração. A refatoração principal envolve a integração com a nova pipeline de processamento de documentos, onde o frontend envia um arquivo PDF para o `pdf_processor_service` (via gateway da API principal) e, em seguida, o backend do `gerador_quesitos` utiliza o `document_id` retornado para buscar o texto processado e gerar os quesitos.

## 2. Escopo do Teste

Este plano cobre:
*   Testes da interface do usuário (Frontend) para upload de arquivos.
*   Testes do endpoint da API (Backend) para geração de quesitos.
*   Testes de integração entre Frontend, Backend da API Principal (gateway), `pdf_processor_service`, e o backend do `gerador_quesitos`.
*   Esboço de cenários para testes End-to-End (E2E).

## 3. Tipos de Teste

*   **Testes de Unidade (Backend):** Foco nas lógicas internas do serviço `gerador_quesitos` (ex: interação com LangChain, busca no banco de dados). (Já cobertos parcialmente em testes anteriores, mas verificar necessidade de novos testes específicos para a refatoração).
*   **Testes de Integração (Backend):** Verificar a comunicação entre o endpoint do `gerador_quesitos` e o `document_service` (para buscar texto do PDF processado).
*   **Testes de Componente (Frontend):** Testar os componentes React responsáveis pelo upload de arquivos e exibição de resultados.
*   **Testes de API (Backend):** Testar diretamente o endpoint `/gerar_quesitos_refatorado` (ou nome similar).
*   **Testes End-to-End (E2E):** Simular o fluxo completo do usuário.

## 4. Detalhamento dos Testes

### 4.1. Testes da Interface do Usuário (Frontend - `gerador_quesitos`)

**Objetivo:** Garantir que o usuário consiga realizar o upload de um arquivo PDF e que a interface reaja adequadamente, comunicando-se com o backend para iniciar o processamento e, posteriormente, a geração de quesitos.

| Caso de Teste ID | Descrição                                                                                                | Passos                                                                                                                                                                                                                                                           | Resultado Esperado                                                                                                                                                                                                                                                        | Prioridade | Tipo         |
| :--------------- | :------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------- | :----------- |
| **GQ-FE-001**    | Upload de PDF válido e início da geração de quesitos.                                                    | 1. Navegar para a página do `gerador_quesitos`. <br> 2. Selecionar um arquivo PDF válido. <br> 3. Clicar no botão "Gerar Quesitos". <br> 4. Inserir o tema/contexto para os quesitos. <br> 5. Submeter.                                                               | O arquivo é enviado. <br> Uma indicação de processamento é exibida. <br> Após o processamento, o endpoint de geração de quesitos é chamado com o `document_id` e o tema. <br> Os quesitos gerados são exibidos na interface.                                                         | Alta       | Componente/E2E |
| **GQ-FE-002**    | Tentativa de upload de arquivo com formato inválido (não PDF).                                           | 1. Navegar para a página do `gerador_quesitos`. <br> 2. Tentar selecionar um arquivo `.txt` ou `.jpg`.                                                                                                                                                              | Uma mensagem de erro é exibida informando que apenas arquivos PDF são permitidos. <br> O botão "Gerar Quesitos" permanece desabilitado ou a submissão é prevenida.                                                                                                            | Média      | Componente   |
| **GQ-FE-003**    | Erro durante o upload do PDF (simulado ou real, e.g., falha de rede, erro no `pdf_processor_service`).       | 1. Navegar para a página do `gerador_quesitos`. <br> 2. Selecionar um PDF válido. <br> 3. Clicar "Gerar Quesitos". (Simular falha na chamada ao gateway de upload).                                                                                                   | Uma mensagem de erro apropriada é exibida ao usuário (e.g., "Falha ao processar o documento. Tente novamente.").                                                                                                                                                           | Média      | Componente   |
| **GQ-FE-004**    | Erro durante a geração de quesitos (simulado ou real, e.g., falha no backend do `gerador_quesitos`).       | 1. Completar o upload do PDF com sucesso. <br> 2. Inserir tema. <br> 3. Submeter para geração de quesitos. (Simular falha na chamada ao backend do `gerador_quesitos`).                                                                                              | Uma mensagem de erro apropriada é exibida ao usuário (e.g., "Falha ao gerar quesitos. Tente novamente.").                                                                                                                                                                 | Média      | Componente   |
| **GQ-FE-005**    | Estado de carregamento/feedback visual durante o processamento do PDF e geração de quesitos.             | 1. Realizar GQ-FE-001.                                                                                                                                                                                                                                           | Indicadores visuais (spinners, mensagens de status) são exibidos durante o upload, processamento do PDF e durante a geração dos quesitos.                                                                                                                                   | Alta       | Componente   |
| **GQ-FE-006**    | Limpar o arquivo selecionado ou os resultados.                                                           | 1. Selecionar um PDF. <br> 2. Verificar se existe opção para remover/limpar a seleção. <br> 3. Após gerar quesitos, verificar se existe opção para limpar os resultados e realizar nova consulta.                                                              | A interface permite ao usuário limpar o arquivo selecionado e/ou os resultados para iniciar um novo processo.                                                                                                                                                            | Baixa      | Componente   |

### 4.2. Testes do Endpoint Backend Refatorado (`gerador_quesitos`)

**Objetivo:** Garantir que o endpoint backend do `gerador_quesitos` processe corretamente as requisições, utilize o `document_id` para buscar o texto, interaja com o modelo de linguagem e retorne os quesitos.

**Endpoint:** `/api/gerador_quesitos/gerar_refatorado` (ou nome similar)
**Método:** `POST`
**Payload Esperado:** `{ "document_id": "uuid_do_documento", "tema": "texto do tema/contexto" }`

| Caso de Teste ID | Descrição                                                                                               | Passos (Requisição)                                                                                                                               | Resultado Esperado (Resposta)                                                                                                                                                                                                                                                             | Prioridade | Tipo    |
| :--------------- | :------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------ |
| **GQ-BE-001**    | Requisição válida com `document_id` existente e tema.                                                   | Enviar POST para o endpoint com `document_id` de um PDF previamente processado e um `tema` válido.                                                | Status `200 OK`. <br> Corpo da resposta contém uma lista de quesitos gerados. <br> Verifica-se (via logs ou mock) que o `document_service` foi chamado para buscar o texto e o `LangChainService` (ou similar) foi usado para gerar os quesitos.                                            | Alta       | API     |
| **GQ-BE-002**    | Requisição com `document_id` inexistente/inválido.                                                      | Enviar POST com um `document_id` que não corresponde a nenhum documento processado.                                                               | Status `404 Not Found` ou `422 Unprocessable Entity`. <br> Mensagem de erro indicando que o documento não foi encontrado ou não pôde ser processado.                                                                                                                                     | Alta       | API     |
| **GQ-BE-003**    | Requisição com `document_id` válido, mas o texto do documento está vazio ou é inadequado.                 | Enviar POST com `document_id` de um PDF cujo texto extraído é vazio ou muito curto.                                                                 | Status `422 Unprocessable Entity` ou `200 OK` com uma mensagem/resultado indicando que não foi possível gerar quesitos (e.g., lista vazia de quesitos e uma observação).                                                                                                                   | Média      | API     |
| **GQ-BE-004**    | Requisição sem `document_id`.                                                                           | Enviar POST sem o campo `document_id` no payload.                                                                                                   | Status `422 Unprocessable Entity`. <br> Mensagem de erro indicando que `document_id` é obrigatório.                                                                                                                                                                        | Média      | API     |
| **GQ-BE-005**    | Requisição sem `tema`.                                                                                  | Enviar POST sem o campo `tema` no payload.                                                                                                        | Status `422 Unprocessable Entity`. <br> Mensagem de erro indicando que `tema` é obrigatório.                                                                                                                                                                               | Média      | API     |
| **GQ-BE-006**    | Erro interno no serviço de geração de quesitos (e.g., falha na comunicação com o modelo de linguagem).    | Simular uma falha no `LangChainService` (ou similar) quando o endpoint do `gerador_quesitos` tentar usá-lo.                                          | Status `500 Internal Server Error`. <br> Mensagem de erro genérica indicando falha no servidor.                                                                                                                                                                          | Média      | API     |
| **GQ-BE-007**    | Teste de carga leve: múltiplas requisições válidas.                                                        | Enviar algumas requisições GQ-BE-001 em sequência.                                                                                                   | Todas as requisições retornam `200 OK` com quesitos. O sistema permanece estável.                                                                                                                                                                                            | Baixa      | API     |

### 4.3. Esboço de Cenários para Testes End-to-End (E2E)

**Objetivo:** Validar o fluxo completo da perspectiva do usuário, desde o upload do PDF até a visualização dos quesitos gerados.

| Cenário ID    | Descrição do Fluxo                                                                                                                                                                                                                                                                                                                                                          | Componentes Envolvidos                                                                                                                                                                                                                                                           | Verificações Chave                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **GQ-E2E-001** | **Fluxo Feliz:** <br> 1. Usuário acessa a página do `gerador_quesitos`. <br> 2. Usuário seleciona um arquivo PDF válido. <br> 3. Usuário clica em "Processar Documento" (ou similar, se o upload e processamento inicial forem etapas separadas). <br> 4. Frontend envia o PDF para o gateway da API Principal. <br> 5. Gateway encaminha para `pdf_processor_service`. <br> 6. `pdf_processor_service` processa o PDF, extrai texto e armazena. <br> 7. `pdf_processor_service` retorna `document_id` para o frontend (via gateway). <br> 8. Frontend exibe mensagem de sucesso do processamento. <br> 9. Usuário insere o "tema" para os quesitos. <br> 10. Usuário clica em "Gerar Quesitos". <br> 11. Frontend envia `document_id` e `tema` para o backend do `gerador_quesitos`. <br> 12. Backend do `gerador_quesitos` busca o texto do documento usando `document_id`. <br> 13. Backend do `gerador_quesitos` usa LangChain para gerar quesitos. <br> 14. Backend retorna os quesitos para o frontend. <br> 15. Frontend exibe os quesitos gerados. | Frontend (`gerador_quesitos` UI) <br> Backend API Principal (Gateway de Documentos) <br> `pdf_processor_service` (Upload, Extração, Armazenamento) <br> Banco de Dados (armazenamento de texto processado) <br> Backend (`gerador_quesitos` service) <br> LangChain Service | O PDF é carregado e processado com sucesso. <br> O `document_id` correto é usado. <br> O texto correto do documento é recuperado. <br> Os quesitos são gerados com base no tema e no conteúdo do PDF. <br> Os quesitos são exibidos corretamente na interface. <br> Não ocorrem erros inesperados durante o fluxo. <br> Feedback visual adequado é fornecido ao usuário em cada etapa. |
| **GQ-E2E-002** | **Fluxo com Falha no Processamento do PDF:** <br> Seguir GQ-E2E-001 até o passo 5. <br> 6. Simular falha no `pdf_processor_service` (e.g., PDF corrompido, erro interno no serviço).                                                                                                                                                                                          | Idem GQ-E2E-001 (até o ponto da falha).                                                                                                                                                                                                                                  | O Frontend exibe uma mensagem de erro clara informando que o processamento do documento falhou. <br> O usuário não consegue prosseguir para a etapa de inserção do tema ou geração de quesitos.                                                                                                                                                                                                                                           |
| **GQ-E2E-003** | **Fluxo com Falha na Geração de Quesitos:** <br> Seguir GQ-E2E-001 até o passo 11. <br> 12. Simular falha no backend do `gerador_quesitos` (e.g., `document_id` não encontrado, erro ao contatar LangChain).                                                                                                                                                                | Idem GQ-E2E-001 (até o ponto da falha).                                                                                                                                                                                                                                  | O Frontend exibe uma mensagem de erro clara informando que a geração de quesitos falhou. <br> Os quesitos não são exibidos.                                                                                                                                                                                                                                                                                                             |

## 5. Ambiente de Teste e Ferramentas

*   **Frontend:**
    *   Navegador: Chrome, Firefox (últimas versões)
    *   Framework de Teste: Jest, React Testing Library (para componentes), Cypress ou Playwright (para E2E).
*   **Backend:**
    *   Ferramenta de Teste de API: Postman, Insomnia, ou scripts `pytest` com `httpx`/`requests`.
    *   Ambiente: Instância local/staging do `pdf_processor_service`, API Principal e `gerador_quesitos_service`.
    *   Banco de Dados: Instância de teste do PostgreSQL (ou similar, conforme configurado).
*   **Dados de Teste:**
    *   Conjunto de arquivos PDF válidos (curtos, longos, com diferentes formatações).
    *   Arquivos PDF inválidos ou corrompidos.
    *   Exemplos de temas/contextos para geração de quesitos.

## 6. Critérios de Entrada/Saída

*   **Critérios de Entrada:**
    *   TASK-058 (Refatoração do `gerador_quesitos`) concluída e código mergeado no branch de desenvolvimento.
    *   Ambiente de teste configurado e acessível.
    *   Dependências (como `pdf_processor_service` e API Principal) implantadas e funcionais no ambiente de teste.
*   **Critérios de Saída:**
    *   Todos os casos de teste definidos (prioridade Alta e Média) executados.
    *   Percentual de sucesso de testes acima de 95% para casos de Alta prioridade.
    *   Defeitos críticos e de alta prioridade corrigidos e retestados.
    *   Relatório de execução de testes preenchido e arquivado.

## 7. Responsabilidades

*   **Desenvolvedor (Jules/Equipe):** Implementação dos testes unitários e de integração.
*   **QA (se aplicável) / Desenvolvedor (Jules/Equipe):** Execução dos testes de API, componentes e E2E. Documentação dos resultados.

## 8. Cronograma (Estimado)

*   Criação e revisão deste plano: X horas
*   Implementação de novos testes (se necessário): Y horas
*   Execução dos testes e relatório: Z horas

## 9. Riscos e Mitigações

*   **Risco:** Atraso na disponibilização do ambiente de teste integrado.
    *   **Mitigação:** Testar componentes e serviços de forma isolada sempre que possível. Comunicação proativa sobre o status do ambiente.
*   **Risco:** Complexidade na simulação de falhas em serviços dependentes.
    *   **Mitigação:** Utilizar mocks e stubs de forma extensiva. Focar em testes de contrato entre os serviços.
*   **Risco:** Inconsistências nos resultados do modelo de linguagem (LangChain).
    *   **Mitigação:** Definir critérios de aceitação flexíveis para a qualidade dos quesitos gerados, focando mais na funcionalidade do fluxo do que na perfeição semântica em todos os casos. Usar prompts e contextos bem definidos.

Este plano de teste será atualizado conforme necessário durante o ciclo de desenvolvimento e teste.
