DOCKER_COMPOSE_PATH = docker-compose.yml
PROJECT_NAME = data-sharding
CMD = src/main.py

start-dev-env:
	docker-compose -f $(DOCKER_COMPOSE_PATH) -p $(PROJECT_NAME) up -d

stop-dev-env:
	docker-compose -f $(DOCKER_COMPOSE_PATH) -p $(PROJECT_NAME) down

dev:
	uv run python $(CMD)