# Docker Summary

This document provides a summary of key Docker concepts and practices relevant to this project, focusing on Dockerfiles, Docker Compose, and best practices.

## Dockerfiles

A `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image.

Key Instructions & Concepts:
- `FROM`: Specifies the base image.
- `WORKDIR`: Sets the working directory for subsequent instructions.
- `COPY` / `ADD`: Copies files/directories into the Docker image. `COPY` is generally preferred.
- `RUN`: Executes commands in a new layer on top of the current image and commits the results. Used for installing packages, etc.
- `CMD` / `ENTRYPOINT`: Specify what command to run when the container starts. `ENTRYPOINT` configures a container that will run as an executable. `CMD` provides defaults for an executing container, which can be overridden.
- `EXPOSE`: Informs Docker that the container listens on the specified network ports at runtime. Does not actually publish the port.
- `ENV`: Sets environment variables.
- `ARG`: Defines build-time variables.

### Multi-stage Builds
Multi-stage builds allow you to use multiple `FROM` statements in your Dockerfile. Each `FROM` instruction can use a different base, and each of them begins a new stage of the build. You can selectively copy artifacts from one stage to another, leaving behind everything you don’t want in the final image. This is extremely useful for creating lean production images by separating build-time dependencies from runtime dependencies.

Example:
```Dockerfile
# Stage 1: Build the application
FROM golang:1.17 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Stage 2: Create the production image
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

### Best Practices for Writing Dockerfiles
- **Keep images small:** Only include necessary files and dependencies. Use multi-stage builds.
- **Use a `.dockerignore` file:** Exclude files and directories not needed for the build (e.g., `.git`, `node_modules` if dependencies are installed in the image).
- **Minimize layers:** Each instruction in the Dockerfile creates a layer. Group related commands (e.g., multiple `RUN` commands for package installation) to reduce the number of layers.
- **Order matters for caching:** Place instructions that change less frequently (like installing dependencies) before instructions that change more frequently (like copying source code) to leverage Docker's build cache effectively.
- **Use official and verified base images:** Start with trusted base images from Docker Hub.
- **Be specific with tags:** Avoid using `latest` tag for base images in production; use specific version tags (e.g., `python:3.9-slim`).
- **Run as non-root user:** Create and switch to a non-root user in the Dockerfile for better security.
- **Understand `CMD` vs `ENTRYPOINT`:** Use them appropriately for your container's purpose.

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file (typically `docker-compose.yml`) to configure the application's services, networks, and volumes.

Key Concepts & Configuration:
- **Services:** Define the different containers that make up your application (e.g., web server, database, message broker). Each service is built from a Dockerfile or a pre-built image.
- **`build` vs `image`:**
    - `build`: Specifies the path to a Dockerfile to build an image for the service.
    - `image`: Specifies a pre-built image to use (e.g., `postgres:15` or `redis:7`).
- **`ports`:** Maps ports from the host to the container (e.g., ` "8080:80"`).
- **`volumes`:** Mounts host paths or named volumes into containers for persistent storage or sharing data (e.g., `db_data:/var/lib/postgresql/data` or `./my_code:/app`).
- **`environment`:** Sets environment variables for services.
- **`depends_on`:** Specifies service dependencies, controlling startup order (though it only waits for the container to *start*, not necessarily for it to be *ready*).
- **`networks`:** Defines custom networks for services to communicate. By default, Compose sets up a single default network for your app.
- **`command`:** Overrides the default command for a service's container.

### Common Docker Compose Commands
- `docker-compose up`: Builds (if necessary), creates, starts, and attaches to containers for an application. Add `-d` to run in detached mode.
- `docker-compose down`: Stops and removes containers, networks, and optionally volumes (with `-v`).
- `docker-compose build [service_name]`: Builds or rebuilds images for services.
- `docker-compose ps`: Lists containers.
- `docker-compose logs [service_name]`: Displays log output from services.
- `docker-compose exec <service_name> <command>`: Executes a command in a running container.
- `docker-compose run <service_name> <command>`: Runs a one-off command on a service (creates a new container).

### Using Compose in Development vs. Production
- **Development:**
    - Use bind mounts for source code to reflect changes immediately.
    - Expose ports for debugging.
    - May use lighter base images or include dev tools.
- **Production:**
    - Avoid bind mounts for application code; code should be built into the image.
    - Don't expose unnecessary ports.
    - Use minimal, secure base images.
    - Manage secrets appropriately (e.g., Docker secrets, environment variables injected securely).
    - Consider using multiple Compose files (e.g., `docker-compose.yml` for base, `docker-compose.override.yml` for development, `docker-compose.prod.yml` for production overrides) to tailor configurations.

References:
- Docker Build: https://docs.docker.com/build/
- Dockerfile Best Practices: https://docs.docker.com/build/building/best-practices/
- Multi-stage Builds: https://docs.docker.com/build/building/multi-stage/
- Docker Compose: https://docs.docker.com/compose/
- Compose File Reference: https://docs.docker.com/compose/compose-file/
