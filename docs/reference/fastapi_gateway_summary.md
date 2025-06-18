# FastAPI Gateway Summary

This document summarizes key FastAPI features and patterns relevant for building an API Gateway, particularly for interacting with other microservices. It draws from the official FastAPI documentation.

## Core Concepts for Gateway Development

- **FastAPI Instance:** The main application object, `app = FastAPI()`.
- **Path Operations:** Functions decorated with `@app.get()`, `@app.post()`, etc., to handle incoming requests.
- **Type Hints & Pydantic:** FastAPI heavily uses Python type hints for data validation, serialization, and documentation. Pydantic models define data shapes.
- **Async Support:** FastAPI is built on Starlette and ASGI, supporting `async` and `await` for non-blocking I/O, crucial for a gateway making requests to other services.

## Structuring with APIRouter (Modules)

For larger applications, `APIRouter` helps organize path operations into modules.

- **Creating a Router:**
  ```python
  # in, e.g., my_module/router.py
  from fastapi import APIRouter

  router = APIRouter(
      prefix="/my-module",
      tags=["My Module"],
      responses={404: {"description": "Not found"}},
  )

  @router.get("/items/")
  async def read_items():
      return [{"name": "Item Foo"}, {"name": "Item Bar"}]
  ```
- **Including Router in Main App:**
  ```python
  # in main.py
  from fastapi import FastAPI
  from my_module import router as my_module_router

  app = FastAPI()
  app.include_router(my_module_router.router)
  ```
- This allows breaking down the gateway into logical sections, each handling a specific microservice or functionality.

## Handling File Uploads (`UploadFile`)

FastAPI uses `UploadFile` for handling file uploads.

- **Example Endpoint:**
  ```python
  from fastapi import FastAPI, File, UploadFile
  from typing import List

  app = FastAPI()

  @app.post("/uploadfiles/")
  async def create_upload_files(files: List[UploadFile] = File(...)):
      # files is a list of UploadFile objects
      # For each file:
      # file.filename: str
      # file.content_type: str
      # file.file: SpooledTemporaryFile (file-like object)
      # await file.read(): reads the entire file content as bytes
      # await file.seek(0): to read again if needed
      # await file.write(data): (less common for uploads)
      # await file.close()

      results = []
      for file in files:
          contents = await file.read() # Read file content
          # Process file content (e.g., save to disk, send to another service)
          results.append({"filename": file.filename, "content_type": file.content_type, "size": len(contents)})
          await file.close() # Important to close the file
      return {"uploaded_files": results}
  ```
- **Considerations for Gateway:** The gateway might receive a file and then need to stream or forward it to a backend microservice using `HTTPX`.

## Making HTTP Requests to Other Services (HTTPX)

FastAPI documentation recommends `HTTPX` for making HTTP requests, especially asynchronous ones from within async path operations.

- **Installation:** `pip install httpx`
- **Basic Async GET Request:**
  ```python
  import httpx
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/call-downstream")
  async def call_downstream_service():
      async with httpx.AsyncClient() as client:
          try:
              response = await client.get("http://downstream-service/some/endpoint")
              response.raise_for_status() # Raises HTTPStatusError for 4xx/5xx responses
              return response.json()
          except httpx.HTTPStatusError as exc:
              # Forward or handle specific errors
              return {"error": "Downstream service error", "details": str(exc)}
          except httpx.RequestError as exc:
              return {"error": "Request to downstream service failed", "details": str(exc)}
  ```
- **Posting Data (e.g., JSON, Files):**
  ```python
  # Posting JSON
  async with httpx.AsyncClient() as client:
      payload = {"key": "value"}
      response = await client.post("http://downstream-service/create", json=payload)
      return response.json()

  # Posting Files (multipart/form-data)
  async def forward_file(file: UploadFile = File(...)):
      async with httpx.AsyncClient() as client:
          files_to_send = {'upload_file': (file.filename, await file.read(), file.content_type)}
          response = await client.post("http://downstream-service/upload", files=files_to_send)
          return response.json()
  ```
- **Timeout Configuration:** Always configure timeouts for external calls.
  ```python
  timeout = httpx.Timeout(10.0, connect=5.0) # 10s total, 5s connect
  async with httpx.AsyncClient(timeout=timeout) as client:
      # ...
  ```

## Authentication and Authorization (Dependencies)

FastAPI's Dependency Injection system is powerful for handling authentication.

- **Example: OAuth2 with Password Bearer (JWT):**
  ```python
  from fastapi import Depends, FastAPI, HTTPException, status
  from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
  from pydantic import BaseModel
  from typing import Optional

  # (Simplified JWT creation and verification - use a robust library like python-jose)
  # This is a placeholder for actual JWT logic
  def verify_token(token: str):
      if token != "fake-super-secret-token": # Replace with actual JWT validation
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid authentication credentials",
              headers={"WWW-Authenticate": "Bearer"},
          )
      return {"username": "testuser"} # Decoded token payload

  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # "token" is the path to your token endpoint

  app = FastAPI()

  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None

  async def get_current_user(token: str = Depends(oauth2_scheme)):
      credentials_exception = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate": "Bearer"},
      )
      try:
          payload = verify_token(token) # Your JWT decoding and validation logic
          username: str = payload.get("username")
          if username is None:
              raise credentials_exception
          # You might fetch user from DB here based on username/sub from token
      except Exception: # Replace with specific JWT exceptions
          raise credentials_exception
      return User(username=username) # Or your actual user model

  @app.post("/token")
  async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
      # Authenticate user (form_data.username, form_data.password)
      # If valid, create and return access token
      # This is highly simplified
      if form_data.username == "johndoe" and form_data.password == "secret":
          # Create JWT token here
          access_token = "fake-super-secret-token"
          return {"access_token": access_token, "token_type": "bearer"}
      raise HTTPException(status_code=400, detail="Incorrect username or password")

  @app.get("/users/me")
  async def read_users_me(current_user: User = Depends(get_current_user)):
      return current_user
  ```
- **Applying to Routers:** Dependencies can be applied at the router level to protect all endpoints within that router.
  ```python
  from fastapi import APIRouter, Depends

  router = APIRouter(dependencies=[Depends(get_current_user)])

  @router.get("/secure-data")
  async def get_secure_data():
      return {"message": "This is secured data!"}
  ```

## Other Relevant Features

- **Request Parameters:** Path parameters (`@app.get("/items/{item_id}")`), Query parameters (`item_id: int, q: Optional[str] = None`).
- **Request Body:** Define Pydantic models for request bodies. FastAPI handles validation and serialization.
- **Response Models:** Define Pydantic models for response bodies using `response_model` in path operation decorators for data validation, filtering, and documentation.
- **Status Codes:** Control HTTP status codes using `status_code` parameter in decorators or by returning `Response` objects directly.
- **Error Handling:** Use `HTTPException` for standard HTTP errors. Custom exception handlers can be defined.
- **Middleware:** For cross-cutting concerns like logging, custom authentication, CORS.

This summary provides a focused overview for building a gateway with FastAPI. For more details, refer to the official FastAPI documentation and the specific sections linked.
```
