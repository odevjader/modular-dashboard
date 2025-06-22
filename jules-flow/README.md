# Jules-Flow System

## Propósito do Sistema

Jules-Flow é um sistema de gerenciamento de microtarefas projetado para ser operado pelo agente de IA, Jules, sob a supervisão de um Desenvolvedor humano. O sistema é inteiramente baseado em arquivos Markdown e visa estruturar e rastrear o trabalho de desenvolvimento realizado por Jules de forma transparente, documentada e com alta qualidade.

## Como Utilizar

### 1. Adicionando ao seu Projeto

Para integrar o Jules-Flow, simplesmente copie o diretório `jules-flow/` completo para a raiz do seu projeto. Após a cópia, adicione e comite os arquivos ao seu repositório Git. Isso estabelecerá o sistema de gerenciamento de tarefas como parte integrante do seu projeto.

### 2. Prompt Inicial para o Agente

Para iniciar o trabalho do agente Jules no projeto, você pode usar os seguintes prompts. Eles instruem o agente a se contextualizar, começar a trabalhar ou retomar o desenvolvimento do projeto de acordo com o fluxo estabelecido.


**Prompt para o Primeiro Uso do Agente Jules:**
```markdown
Olá, Jules. Você está iniciando os trabalhos em um novo projeto. Sua primeira missão é preparar o ambiente `jules-flow` e planejar os passos iniciais. Siga estritamente esta sequência:

1.  **Limpeza do Ambiente**: Verifique o diretório `jules-flow` em busca de resíduos de projetos anteriores.
    * Exclua todos os arquivos das pastas `jules-flow/backlog/` e `jules-flow/done/`.
    * Exclua todos os arquivos de `jules-flow/docs/reference/`.
    * Limpe o conteúdo do arquivo `jules-flow/TASK_INDEX.md`, deixando-o vazio.
    * Execute um commit com a mensagem "Setup: Limpeza inicial do ambiente Jules-Flow." para registrar esta ação.

2.  **Análise e Contextualização**:
    * Examine a estrutura de diretórios e o código-fonte do projeto para entender seu propósito e tecnologias.
    * Estude suas instruções em `jules-flow/INSTRUCTIONS_FOR_JULES.md`.

3.  **Planejamento Inicial**:
    * Leia o arquivo `ROADMAP.md` do projeto.
    * Com base no roadmap, crie as `TASK`s iniciais para a primeira fase do projeto e coloque-as no diretório `jules-flow/backlog/`. Siga todas as regras de criação de tarefas definidas em suas instruções.

4.  **Início dos Trabalhos**:
    * Após concluir o planejamento, anuncie que o setup foi finalizado e informe qual será a primeira `TASK` que você irá executar.
```

**Prompt para a Retomada de Trabalho do Agente Jules:**
```markdown
Olá, Jules. É hora de retomar seu trabalho neste projeto. Para garantir a continuidade e consistência, siga rigorosamente os seguintes passos para se reorientar antes de agir:

1.  **Recuperação de Contexto (Memória)**:
    * **Estado do Projeto**: Analise o estado atual dos arquivos do projeto para identificar as mudanças mais recentes.
    * **Suas Instruções**: Releia rapidamente o arquivo `jules-flow/INSTRUCTIONS_FOR_JULES.md` para relembrar suas diretrizes.
    * **Estado das Tarefas**: Verifique as pastas `jules-flow/backlog/` e `jules-flow/done/` para ter um panorama claro do que está pendente e o que já foi concluído. Preste atenção especial na última tarefa movida para `/done/`.

2.  **Identificação do Ponto de Parada**:
    * Sua tarefa mais crítica agora é determinar o estado exato do trabalho no momento da pausa. A última `TASK` em que você estava trabalhando foi totalmente concluída e movida para `/done/`? Ou você estava no meio de uma tarefa que ainda se encontra no `/backlog/`?
    * Analise o histórico de commits para confirmar qual foi a última tarefa registrada.

3.  **Planejamento da Próxima Ação**:
    * Com base na sua análise, anuncie de forma clara e objetiva qual será sua próxima ação.
        * **Se uma tarefa foi interrompida**: "Estou retomando a TASK-XXX, que foi parcialmente concluída. Meu próximo passo é..."
        * **Se a última tarefa foi concluída**: "A TASK-XXX foi concluída. Estou iniciando agora a próxima tarefa do backlog: TASK-YYY."
    * NÃO refaça trabalho que já está concluído e comitado. NÃO crie tarefas duplicadas.

4.  **Execute**:
    * Prossiga com a execução da ação que você planejou.
```

## Fluxo do Sistema

O fluxo de trabalho no Jules-Flow é centrado em arquivos de tarefa em Markdown e organizado em fases sequenciais para garantir robustez e consistência. Cada épico de desenvolvimento é decomposto em tarefas que seguem este fluxo:

1.  **Fase 1: Descoberta e Pesquisa**
    * Antes de qualquer desenvolvimento, uma `TASK` é criada para pesquisar a documentação mais recente das tecnologias a serem utilizadas. O resultado é compilado em um arquivo de referência salvo em `/jules-flow/docs/reference/`, garantindo que o trabalho seja baseado em informações atuais.

2.  **Fase 2: Execução de Desenvolvimento**
    * Com base na pesquisa e nos requisitos da tarefa, Jules realiza as alterações de código necessárias no branch `jules`. Ao concluir, um "Relatório de Execução" detalhado é preenchido no arquivo da `TASK`.

3.  **Fase 3: Testes Automatizados**
    * Após a implementação, uma nova `TASK` é criada para escrever e executar testes automatizados (unitários, de integração, etc.). Isso valida que as novas funcionalidades funcionam como esperado e que não há regressões no código existente.

4.  **Fase 4: Atualização da Documentação**
    * Ao final de um ciclo de desenvolvimento, uma `TASK` é executada para atualizar toda a documentação do projeto (`README.md`, `ROADMAP.md`, etc.), garantindo que ela permaneça sincronizada com o estado atual do código.

5.  **Fase 5: Verificação de Inconsistências**
    * Como etapa final de um bloco de trabalho, uma `TASK` de revisão é executada para analisar o conjunto de alterações, identificar possíveis inconsistências ou conflitos e, se necessário, criar novas tarefas para correção.

## Estrutura de Pastas

* `/jules_flow/`: Diretório raiz do sistema Jules-Flow.
    * `/backlog/`: Contém tarefas pendentes (arquivos `.md`).
    * `/done/`: Contém tarefas concluídas (arquivos `.md`).
    * `/docs/`: Contém documentação gerada pelo Jules-Flow.
        * `/reference/`: Arquivos de referência criados durante a fase de pesquisa.
    * `/templates/`: Contém o modelo `task_template.md` para novas tarefas.
    * `README.md`: Este arquivo.
    * `INSTRUCTIONS_FOR_JULES.md`: Instruções operacionais para o agente Jules.
    * `TASK_INDEX.md`: Índice e relatório de progresso de todas as tarefas.

## Licença

Este projeto está licenciado sob os termos da Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
