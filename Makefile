# Makefile for managing Docker containers with docker-compose

# Use docker-compose (V1 syntax)
COMPOSE=docker-compose

# Prevent target names from conflicting with filenames
.PHONY: build up start down stop logs ps test shell-api help

# Default target when running 'make'
default: help

# Build or rebuild services
build:
	@echo "Building Docker images..."
	$(COMPOSE) build

# Start services in detached mode
up:
	@echo "Starting Docker containers in detached mode..."
	$(COMPOSE) up -d

# Alias for 'up'
start: up

# Stop and remove containers, networks, volumes, images created by 'up'
down:
	@echo "Stopping and removing Docker containers..."
	$(COMPOSE) down

# Alias for 'down'
stop: down

# View output from containers
logs:
	@echo "Showing logs for Docker containers..."
	$(COMPOSE) logs -f

# List containers managed by compose
ps:
	@echo "Listing Docker containers..."
	$(COMPOSE) ps

# Run backend tests inside the api container
test:
	@echo "Running backend tests..."
	$(COMPOSE) exec api pytest tests/

# Get an interactive shell inside the running api container
shell-api:
	@echo "Opening shell into api container..."
	$(COMPOSE) exec api /bin/sh

# Display help message
help:
	@echo "Makefile Commands:"
	@echo "  make build       Build or rebuild service images"
	@echo "  make up          Start services in detached mode"
	@echo "  make start       Alias for 'up'"
	@echo "  make down        Stop and remove containers, networks"
	@echo "  make stop        Alias for 'down'"
	@echo "  make logs        Follow container logs"
	@echo "  make ps          List running containers"
	@echo "  make test        Run backend tests inside the api container"
	@echo "  make shell-api   Get an interactive shell in the api container"
	@echo "  make help        Show this help message"