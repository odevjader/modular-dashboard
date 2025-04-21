# Módulo: Autenticação e Gerenciamento de Usuários

Este documento descreve as funcionalidades de autenticação (login) e gerenciamento de usuários (CRUD) no Modular Dashboard.

## Status Atual (Abril 2025)

🚧 **Em Desenvolvimento / Parcialmente Bloqueado** 🚧

A estrutura base para autenticação e gerenciamento de usuários **foi implementada no backend**, incluindo:
* Endpoints para login (`/api/auth/v1/login`) e recuperação de dados do usuário logado (`/api/auth/v1/users/me`).
* Endpoints para operações CRUD de usuários por administradores (`/api/auth/v1/admin/users/*`).
* Utilitários para hashing de senha (Passlib/bcrypt) e manipulação de Token JWT (python-jose).
* Dependências FastAPI para validação de token e recuperação de usuário (`core/dependencies.py`).
* Modelos SQLAlchemy (`models/user.py`) e Schemas Pydantic (`modules/auth/v1/schemas.py`).

**⚠️ Bloqueio Atual:** Existe um **bug crítico conhecido no endpoint de login (`/api/auth/v1/login`)** que retorna `401 Unauthorized` (usuário não encontrado), mesmo para usuários de teste criados corretamente no banco. Este bug impede os testes dos endpoints de CRUD de usuários e a integração completa com o frontend.

**Este documento será atualizado significativamente após a resolução do bug e a conclusão dos testes.**

## Endpoints da API (Backend Implementado - Não Testado)

Os seguintes endpoints foram implementados no backend (`backend/app/modules/auth/v1/endpoints.py`), mas aguardam correção do bug de login para serem testados:

* **`POST /api/auth/v1/login`**
    * **Propósito:** Autenticar um usuário com email e senha (via OAuth2PasswordRequestForm).
    * **Retorno Esperado (Sucesso):** Token de acesso JWT.
    * **Status:** Bugado (retorna 401 indevidamente).
* **`GET /api/auth/v1/users/me`**
    * **Propósito:** Retornar informações do usuário atualmente logado (requer token JWT válido).
    * **Dependência:** `get_current_active_user` de `core/dependencies.py`.
    * **Retorno Esperado (Sucesso):** Dados do usuário (ex: email, role, is_active).
* **`POST /api/auth/v1/admin/users`**
    * **Propósito:** Criar um novo usuário (acessível apenas por Admins).
    * **Dependência:** (Futura) `require_admin_user`.
    * **Request Body:** Schema Pydantic com email, senha, role, is_active.
* **`GET /api/auth/v1/admin/users`**
    * **Propósito:** Listar todos os usuários (acessível apenas por Admins).
    * **Dependência:** (Futura) `require_admin_user`.
* **`PUT /api/auth/v1/admin/users/{user_id}`**
    * **Propósito:** Atualizar dados de um usuário existente (acessível apenas por Admins).
    * **Dependência:** (Futura) `require_admin_user`.
* **`DELETE /api/auth/v1/admin/users/{user_id}`**
    * **Propósito:** Deletar um usuário (acessível apenas por Admins).
    * **Dependência:** (Futura) `require_admin_user`.

*(Consulte o Swagger UI em `/docs` para detalhes dos schemas de request/response esperados).*

## Fluxo de Autenticação Esperado (Alto Nível)

1.  Usuário envia email/senha para `/