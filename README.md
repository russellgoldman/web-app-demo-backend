# web-app-demo-backend
## Installation
Please ensure you have the most up-to-date version of Docker installed on your computer. You can install the most recent version [here](https://www.docker.com/).

## Development Environment
### Starting the Environment
To start the development environment, please run `make dev-up` from the root directory of the project. It can be accessed on `http://0.0.0.0:8080`.

This command will boot up the following services (as defined in `docker/compose/docker-compose.dev.yaml`):
- FastAPI Backend Server
- Microsoft SQL Server
- Flyway Migration Server
    - Used to migrate SQL files in the `src/db/mssql/migrations` folder by version number

### View Environment Logs
To view the logs of the running development environment, please run `make dev-logs` from the root directory of the project.

### Stopping the Environment
To stop the running development environment, please run `make dev-down` from the root directory of the project.

### Restart the Environment
To rebuild and subsequently start the development environment (if any changes have been made to the project), please run `make dev-restart` from the root directory of the project.

## Swagger Documentation
To view the Swagger docs, please visit `http://0.0.0.0:8080/docs` once the development environment is running.

## SQL Schema Normalization
A normalized SQL schema has been created and can be found in `src/db/mssql/migrations/V2__create_voice_table.sql`.

The schema has been normalized up to Boyce-Codd Normal Form (BCNF).
