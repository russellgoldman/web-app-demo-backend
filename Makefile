ENV_FILE=.env
DEV_COMPOSE_FILE=docker/compose/docker-compose.dev.yaml
TEST_COMPOSE_FILE=docker/compose/docker-compose.test.yaml

# Development Environment Commands
.PHONY: dev-up
dev-up:
	docker-compose -f $(DEV_COMPOSE_FILE) --env-file ${ENV_FILE} up -d

.PHONY: dev-down
dev-down:
	docker-compose -f $(DEV_COMPOSE_FILE) down

.PHONY: dev-logs
dev-logs:
	docker-compose -f $(DEV_COMPOSE_FILE) logs -f

.PHONY: dev-restart
dev-restart:
	docker-compose -f $(DEV_COMPOSE_FILE) --env-file ${ENV_FILE} up --build -d

# Test Environment Commands
.PHONY: test
test:
	docker-compose -f $(TEST_COMPOSE_FILE) up --build
