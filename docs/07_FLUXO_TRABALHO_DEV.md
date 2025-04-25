#docs/07_FLUXO_TRABALHO_DEV.md
# Fluxo de Trabalho de Desenvolvimento (Experimental V5 - Formalizado)

Este documento descreve o modelo de desenvolvimento colaborativo Humano-IA utilizado no projeto Modular Dashboard, envolvendo Desenvolvedores (Devs) Humanos, o Maestro IA (Orquestrador), e o Agente IA Coder (Integrado ao IDE, ex: RooCode), que agora opera com maior autonomia no detalhamento técnico.

*(Última atualização: 25 de Abril de 2025 - Adotando fluxo experimental V5 e clareza no formato de prompt)*

## Filosofia e Papéis

Mantemos a filosofia de colaboração Humano-IA, mas ajustamos as responsabilidades para otimizar o fluxo, com base em experimentos:

1.  **Dev (Desenvolvedor Humano):**
    * **Centro Estratégico e de Execução:** Define requisitos, coordena, toma decisões finais, gerencia Git (Branches, Commits Frequentes, PRs).
    * **Interface e Supervisor:** Interage com Maestro IA (planejamento, contexto, docs), passa tarefas/abordagem para o Coder IA, **supervisiona ativamente** as ações do Coder, **aprova planos detalhados**, fornece feedback, executa testes de validação finais, opera a ferramenta RooCode (para aplicar docs via prompt do Maestro).
    * **Executor de Comandos:** Executa comandos de terminal (Docker, Git, etc.) quando necessário.
    * **Garantidor do Estado:** **Crucial:** Garante que o repositório esteja em um estado "limpo" (sem alterações não commitadas) antes de iniciar uma nova tarefa com o Coder IA.

2.  **Maestro IA (Orquestrador & Coordenador):**
    * **Planejador e Contextualizador:** Mantém contexto geral, auxilia no planejamento, sugere branches, analisa sumários finais (fornecidos pelo Dev).
    * **Orientador de Alto Nível:** Para cada tarefa, gera:
        * O **objetivo de alto nível** (Issue #).
        * O **contexto relevante**.
        * Uma **lista explícita de documentos** que o Coder IA deve ler *antes* de planejar.
        * Uma **sugestão de abordagem de alto nível** para a solução.
        * **Não fornece mais os passos detalhados** de implementação.
    * **Gerador de Documentação:** Gera prompts RooCode para o Dev aplicar atualizações na **documentação oficial**, seguindo estritamente o formato definido abaixo.
    * **Facilitador:** Gera sumários de sessão, sugere mensagens de commit. NÃO executa código/comandos. Solicita arquivos via `code <path>`.

3.  **Coder IA (Agente IA Coder - Integrado ao IDE, ex: RooCode):**
    * **Implementador Técnico Detalhista:** Recebe objetivo, contexto, lista de docs e abordagem sugerida do Maestro (via Dev).
    * **Planejador Detalhado:** **Lê os documentos indicados primeiro.** Elabora um **plano técnico detalhado** para implementar a abordagem sugerida. Apresenta este plano ao Dev para **aprovação antes de executar**.
    * **Executor Supervisionado:** Implementa o plano aprovado, utilizando suas capacidades de acesso a arquivos e execução de terminal (sob supervisão e confirmação do Dev para ações significativas).
    * **Verificador:** Realiza ou solicita ao Dev os passos necessários para **verificar se a implementação funciona corretamente** antes de finalizar.
    * **Comunicador:** Interage com o Dev para feedback, esclarecimentos e status.
    * **Sumarizador:** Gera o **"Sumário Final para Orquestrador"** detalhado ao concluir.

4.  **RooCode (Ferramenta Integrada ao VS Code):**
    * Atua como o **Coder IA** (Agente Tipo 1).
    * Atua como a ferramenta que o **Dev** usa para aplicar os prompts `Action/Path/Content` gerados pelo **Maestro IA** (para atualização de documentação).

## Formato Padrão de Prompt para RooCode (Gerado pelo Maestro IA para Docs)

Mantém-se o formato para garantir clareza e execução correta pelo RooCode ao aplicar atualizações de documentação:

**Estrutura:**
Linha 1: `Action: [Create File | Overwrite File | Append Lines]`
Linha 2: `Relative Path: [Caminho/Relativo/Do/Arquivo.ext]`
Linha 3: `--- START CONTENT ---`
Linha 4 em diante: Conteúdo completo do arquivo (preservando formatação interna).
Última Linha + 1: `--- END CONTENT ---`

**Observações Cruciais:**
* **Importante:** O conteúdo entre `--- START CONTENT ---` e `--- END CONTENT ---` DEVE ser o conteúdo **completo e exato** do arquivo, sem abreviações ou omissões (ex: não usar '...' ou referências a seções omitidas). O conteúdo é literal.
* **NÃO** usar delimitadores Markdown (```) dentro do bloco de conteúdo (ex: para blocos de código internos como Mermaid, YAML, etc.).
* O Maestro IA apresentará o prompt completo dentro de um bloco ```text no chat apenas para facilitar a cópia pelo Dev. O que deve ser passado ao RooCode é o texto *dentro* desse bloco ```text.
* **Padrão de Primeira Linha:** Todo arquivo modificado via prompt deve ter como primeira linha um comentário com seu caminho relativo: `#caminho/relativo/arquivo.ext` (sem espaço após #).

## Colaboração Multi-Usuário e Versionamento (Git)

O fluxo Git (Feature Branch, Rebase, Commits Frequentes, PRs) permanece o mesmo descrito anteriormente. **Reforça-se a importância de commitar o trabalho concluído antes de iniciar uma nova tarefa com o Coder IA para facilitar a recuperação em caso de problemas.**

## Iniciando uma Sessão de Trabalho

O processo permanece similar:
1. Dev sinaliza início.
2. Dev garante repo atualizado e entra no branch correto. Informa o Maestro.
3. Maestro solicita contexto (docs, `code <path>`) se necessário.
4. Dev define meta(s) / Issue a trabalhar.
5. Maestro confirma e prepara a definição da tarefa (objetivo, docs, abordagem).

## Fluxo de Interação Típico (Refinado)

1.  **Definição da Tarefa (Maestro IA -> Dev):** Maestro gera o objetivo, contexto (incluindo lista explícita de docs relevantes), e sugestão de abordagem de alto nível. Inclui nota para o Dev sobre o modo "ARQUITECT".
2.  **Instrução e Planejamento (Dev -> Coder IA -> Dev):** Dev passa a definição da tarefa ao Coder IA, instruindo a iniciar em modo "ARQUITECT" (ou similar). Coder IA lê os docs indicados, elabora o plano técnico detalhado e apresenta ao Dev para aprovação.
3.  **Execução Supervisionada (Dev <-> Coder IA):** Dev aprova o plano. Coder IA (em modo de execução) implementa o plano passo a passo, solicitando confirmação do Dev para ações chave ou após cada modificação/comando. Dev fornece feedback e supervisão.
4.  **Verificação (Coder IA + Dev):** Coder IA realiza/solicita passos para verificar se a implementação funciona. Dev realiza a validação final.
5.  **Sumarização e Handoff (Coder IA -> Dev -> Maestro IA):** Coder IA gera o "Sumário Final para Orquestrador". Dev salva o sumário em `.logs/task_summaries/` (com Issue # no nome) e cola o conteúdo para o Maestro IA analisar.
6.  **Análise e Preparação Docs (Maestro IA -> Dev):** Maestro IA analisa o sumário. Se ok, gera prompt(s) RooCode para atualizar a **documentação oficial** relevante.
7.  **Aplicação Docs (Dev -> RooCode):** Dev executa o(s) prompt(s) RooCode gerados pelo Maestro para aplicar a documentação. Confirma para o Maestro.
8.  **Commit (Maestro IA -> Dev):** Maestro sugere mensagem de commit. Dev executa `git add .`, `git commit`, `git push`.

## Finalizando uma Sessão de Trabalho

Processo similar ao anterior:
1. Sinalização Dev -> Maestro.
2. Garantir último sumário recebido pelo Maestro.
3. Maestro fornece sumário geral da sessão.
4. **Atualização Docs Pendentes (Importante):** Antes de finalizar, garantir que todos os prompts de documentação gerados pelo Maestro foram aplicados pelo Dev via RooCode.
5. Sugestão de Commit Final (Maestro).
6. Versionamento Final (Dev).

## Comunicação

* **Clareza:** Essencial. Maestro fornece docs explícitos. Coder apresenta plano claro. Dev dá feedback preciso.
* **Confirmações:** `OK`/`K` ainda úteis.
* **Solicitação de Arquivos:** Maestro usa `code <path>`. Coder também pode solicitar via Dev.
* **Feedback:** Fundamental em todas as direções.

*(Este documento agora reflete o fluxo de trabalho Humano-IA atualizado e formalizado para o projeto Modular Dashboard).*