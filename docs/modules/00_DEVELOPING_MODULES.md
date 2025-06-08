# Guia para Desenvolvimento de Novos Módulos - Modular Dashboard

## 1. Introdução

Bem-vindo ao guia de desenvolvimento de módulos para a plataforma Modular Dashboard! Esta plataforma foi projetada com uma filosofia modular para permitir a fácil extensão e integração de novas funcionalidades de forma isolada e organizada.

Um "módulo" no contexto desta plataforma geralmente consiste em:
*   **Componentes Backend:** Endpoints de API, lógica de negócios, modelos de dados e schemas.
*   **Componentes Frontend:** Páginas React, componentes de UI, lógica de estado e interações com a API.

Este guia fornecerá as diretrizes e melhores práticas para criar e integrar seus próprios módulos.

## 2. Convenções de Nomenclatura e Considerações Iniciais

*   **ID do Módulo (`module_id`):**
    *   Use `snake_case` (ex: `meu_novo_modulo`, `processador_pedidos`).
    *   Este ID será usado para nomear diretórios e como identificador único no registro de módulos.
    *   Evite espaços ou caracteres especiais.
*   **Nome do Módulo (`name`):**
    *   Um nome legível para humanos (ex: "Meu Novo Módulo", "Processador de Pedidos").
    *   Usado para exibição na UI e documentação.
*   **Planejamento:**
    *   Defina claramente o escopo do seu módulo.
    *   Quais funcionalidades ele proverá?
    *   Quais dados ele precisará armazenar?
    *   Como ele interagirá com o frontend?
    *   Será um módulo acessível por todos ou apenas por administradores?

## 3. Desenvolvimento de Módulos Backend

### 3.1. Estrutura de Diretórios

Cada módulo backend reside em seu próprio diretório dentro de `backend/app/modules/`.

```
backend/app/modules/
└── your_module_id/            # ID do seu módulo em snake_case
    ├── __init__.py
    ├── endpoints.py           # Definição dos endpoints da API (FastAPI APIRouter)
    ├── schemas.py             # Schemas Pydantic para validação e serialização
    ├── models.py              # Modelos SQLAlchemy (se interagir com o banco)
    ├── services.py            # (Opcional) Lógica de negócios e serviços
    └── tests/                 # (Opcional, mas recomendado) Testes para o módulo
        ├── __init__.py
        └── test_your_module_endpoints.py
```

### 3.2. Definição de Endpoints (`endpoints.py`)

*   Utilize `APIRouter` do FastAPI para agrupar os endpoints do seu módulo.
*   Inclua um prefixo de versão (ex: `/v1`) no seu router para facilitar o versionamento futuro.
*   Siga os padrões RESTful para design de API.
*   Use injeção de dependência do FastAPI (`Depends`) para obter sessões de banco de dados e outras dependências.

**Exemplo (`endpoints.py`):**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import schemas
from . import services # Se você tiver uma camada de serviço
# from . import models # Se precisar interagir diretamente com modelos aqui
from app.core.database import get_db # Para obter a sessão do DB
# from app.core.dependencies import get_current_active_user # Exemplo para rotas protegidas

router = APIRouter(
    prefix="/v1/your_module_id", # Use o ID do seu módulo e versione
    tags=["Your Module Name"]    # Tag para agrupar na documentação OpenAPI
)

@router.post("/", response_model=schemas.YourResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_in: schemas.YourResourceCreate,
    db: AsyncSession = Depends(get_db)
    # current_user: user_model.User = Depends(get_current_active_user) # Exemplo
):
    # new_resource = await services.create_new_resource(db=db, resource_data=resource_in)
    # if not new_resource:
    #     raise HTTPException(status_code=400, detail="Failed to create resource")
    # return new_resource
    pass # Implementação

@router.get("/{resource_id}", response_model=schemas.YourResourceResponse)
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    # resource = await services.get_resource_by_id(db=db, resource_id=resource_id)
    # if not resource:
    #     raise HTTPException(status_code=404, detail="Resource not found")
    # return resource
    pass # Implementação
```

### 3.3. Definição de Schemas Pydantic (`schemas.py`)

*   Defina schemas Pydantic para:
    *   Validação de dados de entrada (request bodies).
    *   Serialização de dados de saída (response models).
    *   Transferência de dados internos (DTOs).
*   **Recomendação:** Use `Field` do Pydantic para adicionar `description` e `example` a cada atributo. Isso melhora significativamente a documentação OpenAPI gerada automaticamente.

**Exemplo (`schemas.py`):**
```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class YourResourceBase(BaseModel):
    name: str = Field(..., min_length=3, description="Name of the resource.", example="My Resource")
    description: Optional[str] = Field(default=None, description="Optional description of the resource.", example="A very useful resource.")

class YourResourceCreate(YourResourceBase):
    pass # Campos adicionais para criação, se houver

class YourResourceUpdate(BaseModel): # Não precisa herdar de Base se for para PATCH
    name: Optional[str] = Field(default=None, min_length=3, description="New name for the resource.")
    description: Optional[str] = Field(default=None, description="New description for the resource.")

class YourResourceResponse(YourResourceBase):
    id: int = Field(..., description="Unique ID of the resource.", example=1)
    created_at: datetime = Field(..., description="Timestamp of creation.")

    class Config:
        from_attributes = True # Para permitir conversão de modelos ORM

class YourResourceListResponse(BaseModel):
    items: List[YourResourceResponse] = Field(..., description="List of resources.")
    total: int = Field(..., description="Total number of resources.", example=100)
    # Adicione campos de paginação se aplicável (page, size, pages)
```

### 3.4. Definição de Modelos SQLAlchemy (`models.py`)

*   Se o seu módulo precisa persistir dados, defina modelos SQLAlchemy que herdem de `app.core.database.Base`.
*   Siga as convenções do SQLAlchemy para definir tabelas, colunas e relacionamentos.
*   **Alembic Migrations:**
    1.  Após definir ou alterar um modelo, você precisará gerar uma nova migração Alembic.
    2.  Execute o comando (no container `api`):
        ```bash
        docker-compose exec api alembic revision -m "create_your_module_tables"
        ```
        Substitua `"create_your_module_tables"` por uma mensagem descritiva.
    3.  Edite o arquivo de migração gerado (em `backend/app/alembic/versions/`) para incluir as operações `op.create_table(...)` e `op.drop_table(...)` para seus novos modelos.
    4.  Aplique a migração:
        ```bash
        docker-compose exec api alembic upgrade head
        ```

**Exemplo (`models.py`):**
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Para default server timestamp

from app.core.database import Base # Importe a Base declarativa

class YourModel(Base):
    __tablename__ = "your_module_resources" # Nome da tabela

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # owner_id = Column(Integer, ForeignKey("users.id")) # Exemplo de relacionamento
    # owner = relationship("User") # Exemplo de relacionamento
```

### 3.5. Camada de Serviço (`services.py` - Opcional)

*   Para separar a lógica de negócios dos endpoints, você pode criar uma camada de serviço.
*   Funções nesta camada tipicamente recebem a sessão do banco de dados (`db: AsyncSession`) e os dados Pydantic, e realizam as operações de CRUD ou outras lógicas.

**Exemplo (`services.py`):**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from . import models
from . import schemas

async def get_resource_by_id(db: AsyncSession, resource_id: int) -> Optional[models.YourModel]:
    stmt = select(models.YourModel).where(models.YourModel.id == resource_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_new_resource(db: AsyncSession, resource_data: schemas.YourResourceCreate) -> models.YourModel:
    db_resource = models.YourModel(**resource_data.model_dump())
    db.add(db_resource)
    await db.commit()
    await db.refresh(db_resource)
    return db_resource
```

### 3.6. Registro do Módulo (`backend/app/config/modules.yaml`)

Para que o backend carregue seu módulo (especificamente seus endpoints), ele precisa ser registrado no arquivo `modules.yaml`.

Adicione uma nova entrada à lista `modules`:
```yaml
modules:
  - id: "auth" # Módulo Core existente
    name: "Authentication"
    description: "Handles user authentication, tokens, and basic user info."
    router_path: "app.core_modules.auth.v1.endpoints.router" # Caminho para o objeto APIRouter
    # enabled: true # Opcional, padrão é true

  - id: "your_module_id"  # O ID do seu módulo
    name: "Your Module Name" # Nome legível
    description: "A brief description of what your module does."
    router_path: "app.modules.your_module_id.endpoints.router" # Caminho para o seu APIRouter
    # enabled: true # Descomente e sete para false para desabilitar o carregamento
```
*   `id`: O identificador único do seu módulo (o mesmo usado no nome do diretório).
*   `name`: Nome legível para listagens ou logs.
*   `description`: Breve descrição.
*   `router_path`: O caminho Python completo para a instância `APIRouter` definida em seu `endpoints.py`.
*   `enabled` (opcional): Se `false`, o módulo não será carregado. Padrão é `true`.

### 3.7. Testes Básicos

*   Crie testes unitários e/ou de integração para seus endpoints e serviços.
*   Utilize `pytest` e `httpx.AsyncClient`.
*   Consulte `backend/tests/test_auth_endpoints.py` para exemplos de testes de API.

## 4. Desenvolvimento de Módulos Frontend

### 4.1. Estrutura de Diretórios

Módulos frontend residem em `frontend/src/modules/`.

```
frontend/src/modules/
└── your_module_id/            # ID do seu módulo em snake_case
    ├── index.ts               # (Opcional) Ponto de entrada para exportações do módulo
    ├── YourModulePage.tsx     # Componente principal da página do módulo
    ├── components/            # (Opcional) Componentes específicos do módulo
    │   └── YourCustomComponent.tsx
    └── services/              # (Opcional) Funções de API específicas do módulo, se não usar api.ts global
    └── state/                 # (Opcional) Lógica de estado (ex: Zustand store)
```

### 4.2. Criação de Componentes de Página (`YourModulePage.tsx`)

*   Crie componentes React para as páginas do seu módulo.
*   Utilize Material UI (MUI) para consistência visual, ou seus próprios estilos.

**Exemplo (`YourModulePage.tsx`):**
```tsx
import React from 'react';
import { Container, Typography, Paper, Button } from '@mui/material';
// Importe serviços de API se necessário
// import { yourModuleApiService } from '../../services/api'; // Ou de ./services/

const YourModulePage: React.FC = () => {
  // const [data, setData] = React.useState(null);

  // React.useEffect(() => {
  //   const fetchData = async () => {
  //     // const result = await yourModuleApiService.getData();
  //     // setData(result);
  //   };
  //   fetchData();
  // }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Your Module Page
        </Typography>
        <Typography variant="body1">
          Conteúdo específico do seu módulo aqui.
        </Typography>
        {/* <pre>{JSON.stringify(data, null, 2)}</pre> */}
        <Button variant="contained" sx={{mt: 2}}>Ação do Módulo</Button>
      </Paper>
    </Container>
  );
};

export default YourModulePage; // Exporte como default para React.lazy
```

### 4.3. Definição de Rotas do Módulo

*   As rotas são definidas no registro do módulo (ver seção 4.6) e são relativas a um `basePath` para o módulo.
*   Utilize `React.lazy()` para carregamento sob demanda (code splitting) dos componentes de página.

### 4.4. Gerenciamento de Estado (Opcional)

*   Para estados complexos ou compartilhados dentro do seu módulo, considere usar Zustand.
*   Crie um store em `your_module_id/state/yourModuleStore.ts`.

### 4.5. Interação com APIs Backend

*   Adicione funções ao `frontend/src/services/api.ts` para interagir com os endpoints do seu módulo backend.
*   Defina interfaces TypeScript para os payloads de request e response, alinhadas com seus schemas Pydantic.

**Exemplo (adição em `frontend/src/services/api.ts`):**
```typescript
// ... outras interfaces ...

export interface YourModuleResource { // Exemplo de interface de resposta
  id: number;
  name: string;
  description?: string;
  created_at: string;
}

export interface YourModuleCreatePayload { // Exemplo de interface de criação
  name: string;
  description?: string;
}

// ... outras funções de API ...

/** Fetches resources for YourModule */
export const getYourModuleResources = async (): Promise<YourModuleResource[]> => {
    return apiClient<YourModuleResource[]>(`/your_module_id/v1/`); // Ajuste o path conforme seu endpoint
};

/** Creates a new resource for YourModule */
export const createYourModuleResource = async (payload: YourModuleCreatePayload): Promise<YourModuleResource> => {
    return apiClient<YourModuleResource>(`/your_module_id/v1/`, {
        method: 'POST',
        body: JSON.stringify(payload),
    });
};
```

### 4.6. Registro do Módulo (`frontend/src/config/moduleRegistry.ts`)

Para que o frontend reconheça seu módulo, suas rotas e links de navegação, ele precisa ser registrado em `moduleRegistry.ts`.

Adicione uma nova entrada ao objeto `moduleRegistry`:
```typescript
import React from 'react'; // Necessário para React.lazy
// Importe ícones do MUI ou use caminhos de string para imagens
import YourModuleIcon from '@mui/icons-material/YourDesiredIcon'; // Exemplo

// ... (definições de ModuleRoute, ModuleConfig, ModuleRegistry) ...

const moduleRegistry: ModuleRegistry = {
  // ... outros módulos ...
  yourModuleId: { // Chave deve ser o ID do seu módulo (camelCase ou como preferir, mas seja consistente)
    name: 'Your Module Name',        // Nome legível para UI
    basePath: '/your-module-path',   // Caminho base para todas as rotas deste módulo
    navIcon: YourModuleIcon,         // Ícone para a navegação (MUI SvgIconComponent ou string path)
    navText: 'Your Nav Text',        // Texto para o link de navegação (default: `name`)
    adminOnly: false,                // `true` se apenas admins podem ver/acessar
    routes: [
      {
        path: '/',                   // Rota relativa ao `basePath` (ex: /your-module-path/)
        component: React.lazy(() => import('../modules/your_module_id/YourModulePage')),
        exact: true,                 // `true` para match exato do path
      },
      // {
      //   path: '/details/:id',    // Exemplo de rota com parâmetro
      //   component: React.lazy(() => import('../modules/your_module_id/YourDetailPage')),
      //   exact: true,
      // },
    ],
  },
};

// ... (funções getModuleRegistry, registerModule, getModule, export default) ...
```
*   **Chave do Objeto:** Um identificador para o seu módulo (ex: `geradorQuesitos`, `meuModulo`).
*   `name`: Nome legível.
*   `basePath`: O prefixo do URL para todas as rotas dentro deste módulo (ex: `/gerador-quesitos`).
*   `routes`: Um array de objetos `ModuleRoute`:
    *   `path`: Relativo ao `basePath`. Se `basePath` é `/meu-modulo` e `path` é `/lista`, a URL final será `/meu-modulo/lista`.
    *   `component`: O componente React da página, carregado com `React.lazy()`. O caminho para o import deve ser relativo a `moduleRegistry.ts`.
    *   `exact` (opcional): Booleano para correspondência exata de rota.
*   `navIcon` (opcional): Um componente de ícone MUI (ex: `<HomeIcon />`) ou uma string para o caminho de uma imagem. Usado na barra de navegação.
*   `navText` (opcional): Texto a ser exibido na barra de navegação. Se omitido, o `name` do módulo será usado.
*   `adminOnly` (opcional): Se `true`, o link de navegação e as rotas do módulo só serão acessíveis/visíveis para usuários com role "admin".

### 4.7. Geração Automática de Navegação

Com o módulo registrado corretamente em `moduleRegistry.ts`:
*   Um link de navegação na barra lateral será automaticamente gerado se `navIcon` e `navText` (ou `name`) forem fornecidos.
*   Cards na `HomePage` também podem ser gerados dinamicamente para módulos acessíveis.
*   As rotas definidas serão automaticamente adicionadas ao roteador principal em `App.tsx`.

### 4.8. Testes Básicos

*   Considere adicionar testes para seus componentes React usando Jest e React Testing Library.
*   Teste a lógica de estado e interações de UI.

## 5. Referência a Módulos Existentes

Para exemplos práticos, consulte a estrutura e implementação dos seguintes módulos:
*   **`test_module`**: Um módulo simples criado para verificar a funcionalidade de registro e roteamento.
    *   Backend: `backend/app/modules/test_module/` (se existir um correspondente)
    *   Frontend: `frontend/src/modules/test_module/`
*   **`01_GERADOR_QUESITOS`**: Um módulo mais complexo (pode estar parcialmente desativado ou refatorado).
    *   Backend: `backend/app/modules/01_GERADOR_QUESITOS/`
    *   Frontend: (Verificar se existe um correspondente em `frontend/src/modules/`)

Analise como eles definem endpoints, schemas, componentes React e como são registrados.

## 6. Checklist de Desenvolvimento de Módulo

**Backend:**
*   [ ] Criar diretório do módulo em `backend/app/modules/your_module_id`.
*   [ ] Definir `endpoints.py` com `APIRouter`.
*   [ ] Definir `schemas.py` com modelos Pydantic (com descrições `Field`).
*   [ ] (Se necessário) Definir `models.py` com modelos SQLAlchemy.
*   [ ] (Se modelos criados/alterados) Gerar e aplicar migrações Alembic.
*   [ ] (Opcional) Implementar `services.py`.
*   [ ] Registrar o módulo em `backend/app/config/modules.yaml` com o `router_path` correto.
*   [ ] Escrever testes.

**Frontend:**
*   [ ] Criar diretório do módulo em `frontend/src/modules/your_module_id`.
*   [ ] Criar componentes de página React (ex: `YourModulePage.tsx`).
*   [ ] (Se necessário) Adicionar funções de API em `frontend/src/services/api.ts` e interfaces correspondentes.
*   [ ] Registrar o módulo em `frontend/src/config/moduleRegistry.ts` com `basePath`, `routes` (usando `React.lazy`), `navIcon`, `navText`, etc.
*   [ ] Escrever testes.

**Ambos:**
*   [ ] Garantir que as convenções de nomenclatura foram seguidas.
*   [ ] Testar a integração completa do módulo.

## 7. Considerações Adicionais

*   **Estilo de Código:** Siga os padrões de linting configurados no projeto (ESLint para frontend, Flake8/Black/Ruff para backend).
*   **Tratamento de Erros:** Implemente tratamento de erros robusto tanto no backend (exceções HTTP apropriadas) quanto no frontend (feedback para o usuário).
*   **Segurança:**
    *   Valide todos os inputs.
    *   Proteja endpoints backend que exigem autenticação ou roles específicas usando dependências FastAPI.
    *   No frontend, use `ProtectedRoute` e `adminOnly` no registro para controlar o acesso.
    *   Esteja ciente de vulnerabilidades comuns (XSS, CSRF, Injeção de SQL, etc.).
*   **Performance:** Otimize queries de banco de dados, use carregamento lazy no frontend, e considere a performance de algoritmos complexos.

---

Este guia deve fornecer uma base sólida para o desenvolvimento de novos módulos. Consulte a equipe ou a documentação de tecnologias específicas para dúvidas mais aprofundadas.
