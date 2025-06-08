#docs/05_MODULARIDADE.md
# Mecanismo de Modularidade V1

Este documento detalha o funcionamento do sistema de modularidade V1 implementado no Modular Dashboard, cobrindo tanto o backend (FastAPI) quanto o frontend (React).

*(Última atualização: $(date +"%d de %B de %Y") - Implementação da V1)*

## Visão Geral

O sistema de modularidade V1 permite que o Modular Dashboard carregue e integre funcionalidades de forma dinâmica, com base em configurações centrais. Isso torna a plataforma mais extensível e manutenível, permitindo que novos módulos sejam adicionados ou removidos sem alterar o código do núcleo da aplicação.

## Backend Modularity (FastAPI)

A modularidade no backend é gerenciada através de um arquivo de configuração YAML e um carregador de módulos Python.

### 1. Configuração de Módulos: \`backend/app/configs/modules.yaml\`

Este arquivo é o coração da descoberta de módulos no backend. Ele define quais módulos estão disponíveis e como devem ser carregados.

**Estrutura de \`modules.yaml\`:**
\`\`\`yaml
# backend/app/configs/modules.yaml
modules:
  - name: "unique_module_name"  # Identificador único para o módulo
    # Caminho Python para o pacote do módulo, relativo a 'app'.
    # Deve apontar para o diretório que contém 'endpoints.py'.
    # Ex: 'modules.meu_modulo.v1' ou 'core_modules.meu_core_modulo.v1'
    path: "modules.nome_do_modulo.versao"
    version: "v1"                 # Versão do módulo (deve corresponder ao último segmento do path)
    description: "Descrição do módulo." # Opcional
    enabled: true                 # true para carregar, false para desabilitar
    router_variable_name: "router" # Nome da instância APIRouter em endpoints.py (default: "router")
    prefix: "/api/prefixo"        # Prefixo da API para este módulo (default: "/<name>/<version>")
    tags: ["Tag1", "Tag2"]        # Tags OpenAPI (default: [name.capitalize()])
\`\`\`

**Campos Detalhados:**
*   \`name\`: Um nome curto e único para o módulo. Usado internamente e para gerar prefixos/tags padrão.
*   \`path\`: O caminho Python completo para o pacote do módulo, começando com \`modules.\` (para módulos plugáveis padrão) ou \`core_modules.\` (para módulos essenciais). O carregador espera encontrar um arquivo \`endpoints.py\` dentro deste caminho (ex: \`app/modules/meu_modulo/v1/endpoints.py\`).
*   \`version\`: A string de versão do módulo (ex: "v1", "v2.alpha"). Geralmente corresponde ao último segmento do \`path\`.
*   \`description\`: Uma breve descrição opcional do que o módulo faz.
*   \`enabled\`: Um booleano. Se \`false\`, o módulo é ignorado pelo carregador.
*   \`router_variable_name\`: O nome da variável que contém a instância \`APIRouter\` no arquivo \`endpoints.py\` do módulo. O padrão é \`"router"\`.
*   \`prefix\`: O prefixo de URL para todas as rotas neste módulo. Se omitido, o padrão é \`/{name}/{version}\`.
*   \`tags\`: Uma lista de strings para as tags OpenAPI associadas às rotas deste módulo. Se omitido, o padrão é \`[name.capitalize()]\`.

### 2. Carregador de Módulos: \`backend/app/core/module_loader.py\`

Este script Python é responsável por:
*   **Ler e Validar \`modules.yaml\`**: Utiliza Pydantic models (\`ModuleConfig\`, \`ModulesConfig\`) para validar a estrutura e os valores de cada definição de módulo. Garante que os caminhos existam e que \`endpoints.py\` esteja presente.
*   **Descobrir Roteadores**: Para cada módulo habilitado, ele importa dinamicamente o arquivo \`endpoints.py\` (ex: \`app.modules.nome_do_modulo.versao.endpoints\`).
*   **Extrair Instâncias \`APIRouter\`**: Obtém a instância \`APIRouter\` (usando \`router_variable_name\`) do módulo importado.
*   **Coletar Informações do Roteador**: Armazena o roteador, prefixo e tags para serem usados pelo \`api_router.py\` principal.

### 3. Integração com a Aplicação

*   **\`backend/app/main.py\`**: Na inicialização da aplicação FastAPI, ele agora chama \`load_modules_config()\` e \`discover_module_routers()\` de \`module_loader.py\`. Embora não passe diretamente os roteadores para \`api_router.py\` (para manter o acoplamento baixo), ele inicia o processo e registra quaisquer erros críticos de carregamento.
*   **\`backend/app/api_router.py\`**: Este arquivo agora é responsável por chamar \`load_modules_config()\` e \`discover_module_routers()\` para obter a lista de informações de roteadores dinâmicos. Em seguida, ele itera sobre esta lista e usa \`api_router.include_router()\` para adicionar cada roteador de módulo à aplicação principal com seu prefixo e tags especificados. As importações estáticas anteriores foram removidas.

### 4. Como Adicionar um Novo Módulo Backend

1.  **Criar a Estrutura do Módulo**:
    *   Crie um novo diretório em \`backend/app/modules/\` (ex: \`meu_novo_modulo\`).
    *   Dentro dele, crie um diretório de versão (ex: \`v1\`).
    *   Adicione um arquivo \`__init__.py\` em \`backend/app/modules/meu_novo_modulo/\` e em \`backend/app/modules/meu_novo_modulo/v1/\`.
    *   Crie um arquivo \`endpoints.py\` em \`backend/app/modules/meu_novo_modulo/v1/\`.
2.  **Definir o Roteador no Módulo**:
    *   Em \`endpoints.py\`, defina uma instância \`APIRouter\` (normalmente chamada \`router\`) e adicione suas rotas a ela.
    \`\`\`python
    # backend/app/modules/meu_novo_modulo/v1/endpoints.py
    from fastapi import APIRouter

    router = APIRouter()

    @router.get("/ola")
    async def dizer_ola():
        return {"message": "Olá do Meu Novo Módulo!"}
    \`\`\`
3.  **Registrar o Módulo em \`modules.yaml\`**:
    *   Adicione uma nova entrada à lista \`modules\` em \`backend/app/configs/modules.yaml\`:
    \`\`\`yaml
      - name: "meu_novo_modulo"
        path: "modules.meu_novo_modulo.v1"
        version: "v1"
        description: "Este é o meu novo e incrível módulo."
        enabled: true
        # prefix: "/custom_prefix" # Opcional
        # tags: ["MeuNovoModulo"] # Opcional
    \`\`\`
4.  **Verificar**: Reinicie a aplicação. O novo módulo e suas rotas devem ser carregados automaticamente. Verifique os logs para confirmação.

## Frontend Modularity (React)

A modularidade no frontend é alcançada através de um registro de módulos central, carregamento lento de componentes (lazy loading) e geração dinâmica de rotas e itens de navegação.

### 1. Registro de Módulos: \`frontend/src/config/moduleRegistry.ts\`

Este arquivo define a estrutura e lista todos os módulos de frontend disponíveis.

**Interface \`FrontendModule\`:**
\`\`\`typescript
// frontend/src/config/moduleRegistry.ts
export interface FrontendModule {
  id: string; // Identificador único (ex: 'home', 'meu-modulo')
  path: string; // Caminho do React Router (ex: '/', '/meu-modulo')
  name: string; // Nome legível para navegação e títulos
  component: React.LazyExoticComponent<React.ComponentType<any>>; // Componente lazy-loaded
  icon?: React.ComponentType<SvgIconProps>; // Ícone MUI para navegação (opcional)
  showInNav: boolean; // Mostrar no menu de navegação principal?
  requiredRole?: string | string[]; // Role(s) para acessar (opcional, ex: 'ADMIN')
  group?: string; // Para agrupar na navegação (opcional, futuro)
}
\`\`\`

**Array \`APP_MODULES\`:**
Uma array de objetos \`FrontendModule\`, onde cada objeto representa um módulo.
\`\`\`typescript
export const APP_MODULES: FrontendModule[] = [
  {
    id: 'meu-modulo',
    path: '/meu-modulo',
    name: 'Meu Módulo',
    component: lazy(() => import('../pages/MeuModuloPage')), // Caminho para o componente da página
    icon: MeuModuloIcon, // Componente de ícone MUI importado
    showInNav: true,
    requiredRole: 'USER', // Exemplo
  },
  // ... outros módulos
];
\`\`\`

### 2. Carregamento Dinâmico de Rotas: \`frontend/src/App.tsx\`

*   \`App.tsx\` agora importa \`APP_MODULES\` de \`moduleRegistry.ts\`.
*   Ele itera sobre \`APP_MODULES\` para gerar dinamicamente componentes \`<Route>\` do React Router.
*   Cada rota usa o \`module.component\` (que é lazy-loaded) envolvido por \`React.Suspense\` para exibir um fallback de carregamento.
*   Se \`module.requiredRole\` estiver definido, a rota é adicionalmente envolvida pelo componente \`ProtectedRoute\` (que foi atualizado para aceitar uma prop \`roles\`).

### 3. Navegação Dinâmica: \`frontend/src/layouts/MainLayout.tsx\`

*   O componente \`MainLayout.tsx\` (especificamente a lógica do seu sidebar) agora usa \`APP_MODULES\` para gerar os itens de navegação.
*   Ele filtra os módulos com base no campo \`showInNav\`.
*   Ele também verifica o \`requiredRole\` de cada módulo contra as roles do usuário atual (obtidas de \`useAuthStore\`). Um módulo só é exibido na navegação se o usuário tiver a role necessária.
*   Os ícones e nomes para os links de navegação são retirados diretamente das definições dos módulos.

### 4. Controle de Acesso Baseado em Role: \`frontend/src/components/ProtectedRoute.tsx\`

*   O componente \`ProtectedRoute.tsx\` foi modificado para aceitar uma prop opcional \`roles\` (string ou array de strings).
*   Se \`roles\` for fornecida para uma rota, \`ProtectedRoute\` verifica se o usuário autenticado (de \`useAuthStore\`) possui pelo menos uma das roles especificadas.
*   Se o usuário não estiver autenticado ou não tiver a role necessária, ele é redirecionado (para \`/login\` ou para uma página de "não autorizado"/página inicial, respectivamente).

### 5. Como Adicionar um Novo Módulo Frontend

1.  **Criar Componentes do Módulo**:
    *   Crie o(s) seu(s) componente(s) de página principal para o módulo (ex: em \`frontend/src/pages/NovaPagina.tsx\`).
    *   Crie ou escolha um ícone MUI para o seu módulo.
2.  **Registrar o Módulo em \`moduleRegistry.ts\`**:
    *   Importe o componente de ícone e o componente de página (via \`lazy\`) em \`moduleRegistry.ts\`.
    *   Adicione um novo objeto \`FrontendModule\` ao array \`APP_MODULES\`:
    \`\`\`typescript
    // Em frontend/src/config/moduleRegistry.ts
    import NovoIcon from '@mui/icons-material/Star'; // Exemplo
    // ...
    export const APP_MODULES: FrontendModule[] = [
      // ... módulos existentes
      {
        id: 'nova-pagina',
        path: '/nova-pagina',
        name: 'Nova Página Dinâmica',
        component: lazy(() => import('../pages/NovaPagina')),
        icon: NovoIcon,
        showInNav: true,
        // requiredRole: 'ADMIN', // Opcional
      },
    ];
    \`\`\`
3.  **Verificar**:
    *   A nova rota deve funcionar automaticamente.
    *   Se \`showInNav: true\` e os requisitos de role (se houver) forem atendidos, o módulo aparecerá na navegação da barra lateral.

## Considerações Adicionais

*   **Core Modules vs. Pluggable Modules**: No backend, \`core_modules\` são aqueles essenciais para a plataforma (como \`auth\`, \`health\`). \`modules\` são para funcionalidades de domínio específicas. Ambos os tipos agora são carregados através do \`modules.yaml\`. No frontend, essa distinção é menos sobre o carregamento e mais sobre a organização lógica e dependências.
*   **Comunicação Inter-Módulos**: A V1 foca no carregamento e apresentação independentes de módulos. A comunicação direta entre módulos plugáveis não é um recurso primário desta versão e exigiria mecanismos adicionais (ex: eventos globais, serviços compartilhados via Zustand).
*   **Estilo e UI**: Módulos de frontend devem, idealmente, seguir as diretrizes de UI/UX e usar os componentes do Material UI para consistência, mas têm flexibilidade para construir sua própria UI interna.

Este sistema de modularidade V1 estabelece uma base sólida para futuras expansões e um desenvolvimento mais ágil de novas funcionalidades.
