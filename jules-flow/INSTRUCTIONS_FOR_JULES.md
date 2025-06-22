# Instruções de Operação para Jules

Este documento detalha os princípios e o fluxo de trabalho que você, Jules, deve seguir estritamente para o desenvolvimento de projetos. Seu propósito é garantir um desenvolvimento transparente, rastreável, documentado e de alta qualidade.

## Princípios Gerais

1.  **Comunicação Formal**: Você não deve usar emojis em nenhuma comunicação, documentação ou código. A comunicação deve ser clara, técnica e direta.
2.  **Formato de Arquivo Padrão**: Todos os arquivos de documentação, tarefas e relatórios que você criar devem ser escritos em Markdown e utilizar a extensão `.md`.
3.  **Commit Atômico**: Cada `TASK` concluída deve resultar em um único commit atômico. Este commit deve conter todas as alterações relacionadas à tarefa: modificações de código, atualizações nos arquivos de tarefa, criação de testes e atualizações na documentação.

## O Fluxo de Trabalho por Fases

Seu trabalho será organizado em uma sequência de fases e `TASK`s. O planejamento inicial de um épico deve prever a criação de todas as tarefas necessárias, incluindo desenvolvimento, pesquisa, testes e documentação.

### Fase 1: Descoberta e Pesquisa

* **Objetivo**: Antes de iniciar o desenvolvimento de uma nova funcionalidade, você deve garantir que possui o conhecimento mais atualizado.
* **Ação**:
    1.  Crie uma `TASK` específica para pesquisa. O título deve ser claro, como "TASK-XXX: Pesquisa de Documentação para [Nome da Biblioteca/SDK]".
    2.  Execute uma busca aprofundada pela documentação oficial e atualizada das ferramentas, bibliotecas, SDKs ou serviços que serão utilizados.
    3.  Compile os resultados dessa pesquisa (links, exemplos de código, guias de melhores práticas) em um arquivo de referência.
    4.  Salve este arquivo em `jules-flow/docs/reference/` com um nome descritivo, por exemplo, `referencia-autenticacao-jwt.md`.

### Fase 2: Execução de Desenvolvimento

* **Objetivo**: Implementar as modificações de código, configuração ou infraestrutura conforme descrito na `TASK` de desenvolvimento.
* **Ação**:
    1.  Selecione uma `TASK` de desenvolvimento do `backlog/`.
    2.  Realize as alterações de código necessárias para cumprir os critérios de aceitação.
    3.  Preencha o "Relatório de Execução" no arquivo da `TASK`, detalhando o que foi feito.

### Fase 3: Testes Automatizados

* **Objetivo**: Garantir que as novas modificações não introduziram regressões ou bugs e que a funcionalidade se comporta como esperado.
* **Ação**:
    1.  Imediatamente após a conclusão de uma `TASK` de desenvolvimento, crie uma nova `TASK` para a escrita de testes. Exemplo: "TASK-XXX: Escrita de Testes para [Funcionalidade Implementada]".
    2.  Nesta `TASK`, escreva os testes automatizados (unitários, de integração, etc.) necessários para validar as alterações realizadas na tarefa anterior.
    3.  Execute os testes e anexe os resultados ou um resumo no "Relatório de Execução" da `TASK` de teste.

### Fase 4: Atualização da Documentação

* **Objetivo**: Manter a documentação do projeto sincronizada com o estado atual do código.
* **Ação**:
    1.  No final de cada fase de desenvolvimento significativa (ou conforme planejado no início), execute as `TASK`s de documentação.
    2.  Atualize todos os documentos relevantes: `README.md`, `ROADMAP.md`, e os documentos de referência em `docs/reference/`.
    3.  O "Relatório de Execução" desta `TASK` deve listar todos os documentos que foram atualizados.

### Fase 5: Verificação de Inconsistências

* **Objetivo**: Realizar uma verificação de sanidade ao final de um bloco de desenvolvimento para identificar e corrigir possíveis inconsistências introduzidas por múltiplas alterações.
* **Ação**:
    1.  Ao final de um conjunto de tarefas relacionadas (um "épico" ou "bloco de desenvolvimento"), execute uma `TASK` de "Avaliação de Inconsistências".
    2.  Nesta `TASK`, revise o código e a documentação em busca de conflitos, duplicações ou lógicas contraditórias.
    3.  Documente quaisquer inconsistências encontradas e, se possível, crie novas `TASK`s para corrigi-las.
