DEV_COMPOSE_FILE=docker/compose/docker-compose.dev.yaml
# TEST_COMPOSE_FILE=
# STAGING_COMPOSE_FILE=

# Development Environment Commands
.PHONY: dev-up
dev-up:
	docker-compose -f $(DEV_COMPOSE_FILE) up -d

.PHONY: dev-down
dev-down:
	docker-compose -f $(DEV_COMPOSE_FILE) down

.PHONY: dev-logs
dev-logs:
	docker-compose -f $(DEV_COMPOSE_FILE) logs -f

.PHONY: dev-restart
dev-restart:
	docker-compose -f $(DEV_COMPOSE_FILE) up --build -d
