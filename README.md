# web-app-demo-backend
## Installation
Please ensure you have the most up-to-date version of Docker installed on your computer. You can install the most recent version [here](https://www.docker.com/).

## Development Environment
### Starting the Environment
To start the development environment, please run `make dev-up`. It can be accessed on `http://0.0.0.0:8080`.

This command will boot up the following services (as defined in `docker/compose/docker-compose.dev.yaml`):
- FastAPI Backend Server

### View Environment Logs
To view the logs of the running development environment, please run `make dev-logs`.

### Stopping the Environment
To stop the running development environment, please run `make dev-down`.

## Restart the Environment
To rebuild and subsequently start the development environment (if any changes have been made to the project), please run `make dev-restart`.
