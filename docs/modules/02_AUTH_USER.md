# Módulo: Autenticação e Gerenciamento de Usuários

Este documento descreve as funcionalidades de autenticação (login) e gerenciamento de usuários (CRUD) no Modular Dashboard.

## Status Atual (Junho 2025)

✅ **Funcional**

A estrutura base para autenticação e gerenciamento de usuários está implementada e funcional no backend e no frontend. O bug crítico de login que anteriormente impedia o progresso foi **resolvido** através da correta configuração do ambiente de desenvolvimento (Proxy do Vite e limpeza de ambiente).

**Funcionalidades Implementadas e Verificadas:**
* Endpoints para login (`/api/auth/v1/login`) e recuperação de dados do usuário logado (`/api/auth/v1/users/me`).
* Endpoints para operações CRUD de usuários por administradores (`/api/auth/v1/admin/users/*`).
* Utilitários para hashing de senha (Passlib/bcrypt) e manipulação de Token JWT (python-jose).
* Dependências FastAPI para validação de token e recuperação de usuário.
* Interface de Login no frontend que se comunica com o backend.
* Rotas protegidas que redirecionam para o login caso o usuário não esteja autenticado.

## Endpoints da API

Os seguintes endpoints foram implementados e estão operacionais:

* **`POST /api/auth/v1/login`**
    * **Propósito:** Autenticar um usuário com email e senha.
    * **Retorno (Sucesso):** Token de acesso JWT.
    * **Status:** ✅ Funcional.
* **`GET /api/auth/v1/users/me`**
    * **Propósito:** Retornar informações do usuário atualmente logado (requer token JWT válido).
    * **Status:** ✅ Funcional.
* **`POST /api/auth/v1/admin/users`**
    * **Propósito:** Criar um novo usuário (acessível apenas por Admins).
    * **Status:** ✅ Funcional (backend).
* **`GET /api/auth/v1/admin/users`**
    * **Propósito:** Listar todos os usuários (acessível apenas por Admins).
    * **Status:** ✅ Funcional (backend).
* **`PUT /api/auth/v1/admin/users/{user_id}`**
    * **Propósito:** Atualizar dados de um usuário existente (acessível apenas por Admins).
    * **Status:** ✅ Funcional (backend).
* **`DELETE /api/auth/v1/admin/users/{user_id}`**
    * **Propósito:** Deletar um usuário (acessível apenas por Admins).
    * **Status:** ✅ Funcional (backend).

*(Consulte o Swagger UI em `/docs` para detalhes dos schemas de request/response).*

## Próximos Passos para o Módulo

* Desenvolver a interface de frontend para o gerenciamento de usuários (CRUD) na área de administração.
* Refinar o tratamento de erros e feedback para o usuário no frontend.