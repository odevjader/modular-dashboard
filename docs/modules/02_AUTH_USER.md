# docs/modules/02_AUTH_USER.md
# Módulo: Autenticação e Gerenciamento de Usuários

Este documento descreve as funcionalidades de autenticação (login) e gerenciamento de usuários (CRUD) no Modular Dashboard.

## Funcionalidades Principais
A estrutura base para autenticação e gerenciamento de usuários está implementada e funcional. Isso inclui:
* Endpoints para login e recuperação de dados do usuário logado.
* Endpoints para operações CRUD de usuários por administradores.
* Utilitários para hashing de senha e manipulação de Token JWT.
* Dependências FastAPI para validação de token e recuperação de usuário.
* Interface de Login no frontend e rotas protegidas.

## Endpoints da API

*(Consulte o Swagger UI em `/docs` na API em execução para detalhes completos dos schemas de request/response).*

### Autenticação
* **`POST /api/auth/v1/login`**
    * **Propósito:** Autenticar um usuário com email e senha.
    * **Retorno (Sucesso):** Token de acesso JWT.
    * **Status:** ✅ Funcional.
* **`GET /api/auth/v1/users/me`**
    * **Propósito:** Retornar informações do usuário atualmente logado (requer token JWT válido).
    * **Status:** ✅ Funcional.

### Gerenciamento de Usuários (Admin)
Os seguintes endpoints são acessíveis apenas por usuários com role `ADMIN`:
* **`POST /api/auth/v1/admin/users`**
    * **Propósito:** Criar um novo usuário.
    * **Status:** ✅ Funcional (backend).
* **`GET /api/auth/v1/admin/users`**
    * **Propósito:** Listar todos os usuários.
    * **Status:** ✅ Funcional (backend).
* **`PUT /api/auth/v1/admin/users/{user_id}`**
    * **Propósito:** Atualizar dados de um usuário existente.
    * **Status:** ✅ Funcional (backend).
* **`DELETE /api/auth/v1/admin/users/{user_id}`**
    * **Propósito:** Deletar um usuário.
    * **Status:** ✅ Funcional (backend).

## Próximos Passos para o Módulo

* Desenvolver a interface de frontend para o gerenciamento de usuários (CRUD) na área de administração.
* Refinar o tratamento de erros e feedback para o usuário no frontend.