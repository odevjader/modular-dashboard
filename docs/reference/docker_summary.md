# Docker & Docker Compose Summary

This document provides a comprehensive summary of key Docker concepts and practices relevant to this project, focusing on Dockerfiles, Docker Compose, best practices, and specific examples for a Python/FastAPI application.

## Key Documentation URLs

*   **Docker Documentation:** [https://docs.docker.com/](https://docs.docker.com/)
*   **Docker Build (Dockerfiles):** [https://docs.docker.com/build/](https://docs.docker.com/build/)
*   **Dockerfile Best Practices:** [https://docs.docker.com/build/building/best-practices/](https://docs.docker.com/build/building/best-practices/)
*   **Multi-Stage Builds:** [https://docs.docker.com/build/building/multi-stage/](https://docs.docker.com/build/building/multi-stage/)
*   **Python Specific Guide (Containerize):** [https://docs.docker.com/guides/python/containerize/](https://docs.docker.com/guides/python/containerize/)
*   **Docker Compose Documentation:** [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
*   **Compose File Reference:** [https://docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/) ([Older link: https://docs.docker.com/reference/compose-file/](https://docs.docker.com/reference/compose-file/))
*   **Compose Quickstart:** [https://docs.docker.com/compose/gettingstarted/](https://docs.docker.com/compose/gettingstarted/)

## Dockerfiles

A `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image.

### Key Dockerfile Instructions & Concepts:
- `FROM`: Specifies the base image. (e.g., `python:3.11-slim`)
- `WORKDIR`: Sets the working directory for subsequent instructions within the Docker image. (e.g., `WORKDIR /app`)
- `COPY` / `ADD`: Copies files/directories from the host into the Docker image. `COPY` is generally preferred for its explicitness. (e.g., `COPY ./src /app/src`)
- `RUN`: Executes commands in a new layer on top of the current image and commits the results. Used for installing packages, creating directories, etc. (e.g., `RUN pip install -r requirements.txt`)
- `CMD` / `ENTRYPOINT`: Specify what command to run when the container starts.
    - `ENTRYPOINT`: Configures a container that will run as an executable. Useful for creating images that have a primary command.
    - `CMD`: Provides defaults for an executing container. These defaults can include an executable, or they can specify parameters to an `ENTRYPOINT`. `CMD` can be easily overridden when starting a container.
- `EXPOSE`: Informs Docker that the container listens on the specified network ports at runtime. It does not actually publish the port; it functions as documentation between the person who builds the image and the person who runs the container. (e.g., `EXPOSE 8000`)
- `ENV`: Sets environment variables within the image. These variables are available to subsequent instructions and to the application running in the container. (e.g., `ENV PYTHONDONTWRITEBYTECODE=1`)
- `ARG`: Defines build-time variables. These are only available during the build process and not to the running container unless also set with `ENV`. (e.g., `ARG PYTHON_VERSION=3.11`)

### Multi-stage Builds
Multi-stage builds allow you to use multiple `FROM` statements in your Dockerfile. Each `FROM` instruction can use a different base, and each of them begins a new stage of the build. You can selectively copy artifacts from one stage to another (using `COPY --from=<stage_name> ...`), leaving behind everything you don’t want in the final image. This is extremely useful for creating lean production images by separating build-time dependencies from runtime dependencies.

**Conceptual Example (Python/FastAPI):**
```Dockerfile
# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11
ARG APP_PORT=8000

# ---- Builder Stage ----
# Use a full Python image for building dependencies, including any C extensions.
FROM python:${PYTHON_VERSION} AS builder
LABEL stage=builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/venv
RUN python -m venv .

# Activate venv and install dependencies
COPY requirements.txt .
RUN . /opt/venv/bin/activate && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Runtime Stage ----
# Use a slim Python image for the final runtime environment.
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_PORT=${APP_PORT}

WORKDIR /app

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy virtual environment with dependencies from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
# Adjust paths if your application structure is different (e.g. `COPY . /app` if main.py is in root)
COPY ./src /app/src

USER appuser

EXPOSE ${APP_PORT}

# Activate venv in CMD and run the application
CMD ["/opt/venv/bin/python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "${APP_PORT}"]
```

### Best Practices for Writing Dockerfiles
- **Keep images small:** Only include necessary files and dependencies. Use multi-stage builds and minimal base images (like `-slim` variants).
- **Use a `.dockerignore` file:** Exclude files and directories not needed for the build (e.g., `.git`, `.venv`, `__pycache__`, test files, local `.env` files not intended for the image, `*.md` files).
- **Minimize layers:** Each instruction in the Dockerfile creates a layer. Group related commands (e.g., multiple `RUN` commands for package installation using `&& \`) to reduce the number of layers.
- **Order matters for caching:** Place instructions that change less frequently (like installing dependencies from `requirements.txt`) before instructions that change more frequently (like copying source code) to leverage Docker's build cache effectively.
- **Use official and verified base images:** Start with trusted base images from Docker Hub or your organization's registry.
- **Be specific with tags:** Avoid using `latest` tag for base images in production; use specific version tags (e.g., `python:3.11-slim-bullseye`). Consider pinning to SHA digests for maximum reproducibility.
- **Run as non-root user:** Create and switch to a non-root user in the Dockerfile for better security. Avoid running applications as root inside the container.
- **Understand `CMD` vs `ENTRYPOINT`:** Use them appropriately. `ENTRYPOINT` is good for defining the main executable, while `CMD` can provide default arguments that are easily overridden. For running applications like Uvicorn, `CMD ["executable", "arg1", "arg2"]` (exec form) is common.
- **Use `ENV` for environment variables:** `ENV PYTHONDONTWRITEBYTECODE=1` prevents `.pyc` files, and `ENV PYTHONUNBUFFERED=1` ensures logs are sent directly to stdout/stderr for easier debugging with `docker logs`.
- **Dependency Management:** Copy `requirements.txt` first, then install. For advanced caching with BuildKit, consider `RUN --mount=type=cache,target=/root/.cache/pip ...`.
- **Clean up:** Remove unnecessary files or build artifacts within the same `RUN` instruction to keep layers small (e.g., `apt-get clean` after `apt-get install`).

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file (typically `compose.yaml` or `docker-compose.yml`) to configure the application's services, networks, and volumes.

### Key Compose Concepts & Configuration:
- **Services:** Define the different containers that make up your application (e.g., `api`, `db`, `redis`). Each service is built from a Dockerfile or a pre-built image.
- **`build` vs `image`:**
    - `build`: Specifies the path to a Dockerfile (or a directory containing one) to build an image for the service. (e.g., `build: .` or `build: context: ./backend`)
    - `image`: Specifies a pre-built image to use from a registry like Docker Hub. (e.g., `image: postgres:16-alpine` or `image: redis:7-alpine`)
- **`ports`:** Maps ports from the host machine to ports inside the container (`"HOST_PORT:CONTAINER_PORT"`). (e.g., `ports: - "8000:8000"`)
- **`volumes`:** Mounts host paths or named volumes into containers for persistent storage or sharing data.
    - **Named volumes:** Managed by Docker, good for persistent data like databases (e.g., `volumes: - db_data:/var/lib/postgresql/data`).
    - **Bind mounts:** Mounts a directory or file from the host into the container. Useful for development to see code changes live (e.g., `volumes: - ./src:/app/src`). Avoid for production images where code should be part of the image.
- **`environment` / `env_file`:**
    - `environment`: Sets environment variables directly in the Compose file (e.g., `environment: - DB_HOST=db`).
    - `env_file`: Specifies a path to an environment file (e.g., `.env`) to load variables from. (e.g., `env_file: - .env`). Variables in the `.env` file should typically not be committed to version control if they contain secrets.
- **`depends_on`:** Specifies service dependencies, controlling startup order. Compose starts dependencies first. For more robust control, use with `condition`:
    - `condition: service_started`: Waits for the depended-on container to start.
    - `condition: service_healthy`: Waits for the depended-on service to report as healthy via its `healthcheck`.
    - `condition: service_completed_successfully`: Waits for a one-off task container to exit successfully.
- **`networks`:** Defines custom networks for services to communicate. By default, Compose sets up a single default bridge network for your app. Services on the same network can reach each other by their service name.
- **`command`:** Overrides the default command specified by the Docker image (e.g., `CMD` in Dockerfile).
- **`restart` policy:** Defines what Docker should do if a container exits (e.g., `no`, `always`, `on-failure`, `unless-stopped`). `unless-stopped` is common for long-running services.
- **`healthcheck`:** Defines how to check if a service is healthy (e.g., for a database, check if it's ready to accept connections).

### Example `compose.yaml` for a Python/FastAPI App with PostgreSQL

```yaml
# compose.yaml
version: '3.8' # Or a newer compatible version

services:
  api:
    build:
      context: . # Assuming Dockerfile is in the current directory
      dockerfile: Dockerfile
      args: # Example of passing build ARGs
        PYTHON_VERSION: 3.11
        APP_PORT: 8000
    image: my_fastapi_app:latest # Optionally tag the built image
    container_name: fastapi_app_api
    restart: unless-stopped
    ports:
      - "${API_PORT_HOST:-8000}:${APP_PORT:-8000}" # APP_PORT is from Dockerfile ARG/ENV
    env_file:
      - .env # For DB_USER, DB_PASSWORD, DB_NAME, OPENAI_API_KEY etc.
    environment:
      - DB_HOST=db # Service name of the PostgreSQL container
      - DB_PORT=5432
      # Other non-secret env vars can go here
    depends_on:
      db:
        condition: service_healthy # Wait for DB to be healthy
    networks:
      - app_net
    # For development, to see code changes live (if uvicorn --reload is used in CMD):
    # volumes:
    #   - ./src:/app/src # Mount your source code

  db:
    image: postgres:16-alpine
    container_name: app_postgres_db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - app_db_data:/var/lib/postgresql/data # Named volume for persistence
    ports:
      - "${DB_PORT_HOST:-5433}:5432" # Expose DB port to host if needed for direct access
    networks:
      - app_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s # Give DB time to start up before first healthcheck

volumes:
  app_db_data: # Defines the named volume

networks:
  app_net: # Defines the custom bridge network
    driver: bridge
```
**Note on `.env` file for the example above:**
```env
# .env file (This file should be in .gitignore if it contains secrets)
PYTHON_VERSION=3.11
APP_PORT=8000
API_PORT_HOST=8000

DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=mydb
DB_PORT_HOST=5433 # Host port for DB if direct access needed

# Other environment variables as needed
OPENAI_API_KEY=your_openai_api_key_here
```

### Common Docker Compose Commands
- `docker-compose up`: Builds (if necessary), creates, starts, and attaches to containers for an application. Add `-d` to run in detached mode.
- `docker-compose down`: Stops and removes containers, networks, and optionally volumes (with `-v` or `--volumes`).
- `docker-compose build [service_name]`: Builds or rebuilds images for services.
- `docker-compose ps`: Lists containers for the current Compose project.
- `docker-compose logs [service_name]`: Displays log output from services. Use `-f` to follow logs.
- `docker-compose exec <service_name> <command>`: Executes a command in a running container (e.g., `docker-compose exec api bash`).
- `docker-compose run <service_name> <command>`: Runs a one-off command on a service (creates a new container for it). Useful for tasks like database migrations.
- `docker-compose pull [service_name]`: Pulls service images from the registry.
- `docker-compose stop [service_name]`: Stops running containers without removing them.
- `docker-compose start [service_name]`: Starts existing stopped containers.
- `docker-compose restart [service_name]`: Restarts service containers.
- `docker-compose config`: Validates and views the compiled Compose configuration.

### Using Compose in Development vs. Production
- **Development:**
    - Use bind mounts for source code to reflect changes immediately (e.g., `volumes: - ./src:/app/src`).
    - Expose ports for debugging and direct access.
    - May use lighter base images or include development-specific tools in the Dockerfile (perhaps via a dev stage).
    - `docker-compose.override.yml` can be used to add or modify configuration for development (e.g., add bind mounts, expose different ports).
- **Production:**
    - Avoid bind mounts for application code; code should be built into the image for immutability.
    - Don't expose unnecessary ports to the host or externally.
    - Use minimal, secure base images.
    - Manage secrets appropriately (e.g., Docker secrets, environment variables injected securely via CI/CD or orchestration platform, not hardcoded in `.env` files committed to the repo).
    - Consider using multiple Compose files (e.g., a base `docker-compose.yml`, and a `docker-compose.prod.yml` for production-specific overrides like different restart policies, no debug tools, etc.). Load with `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`.

### Integration with a Larger Project (e.g., `modular-dashboard-adv`)
When integrating a service like `transcritor-pdf` into a larger `docker-compose.yml` setup:
1.  The `transcritor-pdf` API service definition would be added to the main `compose.yaml`.
2.  The `build.context` for `transcritor-pdf` would need to be the relative path from the main Compose file to the `transcritor-pdf` project directory (e.g., `build: ./services/transcritor-pdf`).
3.  If the larger project already provides a PostgreSQL database or Redis instance, the `transcritor-pdf` service would be configured to use those existing services (update `DB_HOST`, `REDIS_HOST` env vars) instead of defining its own.
4.  Services would need to be on a shared Docker network to communicate if they are not already on the default Compose project network.
5.  Environment variable management needs to be consistent and might be centralized in the main project's `.env` file or configuration.

This merged summary should provide a solid foundation for using Docker and Docker Compose.
