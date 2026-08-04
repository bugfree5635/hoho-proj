# CI/CD Deployment

## Overview

This project uses GitHub Actions to automate the Continuous Integration (CI) process.

The current pipeline validates application changes by:

- Installing Python dependencies
- Starting a PostgreSQL test database
- Running automated tests
- Verifying application functionality


Current workflow:

```
Developer

    |
    |
 git push / Pull Request

    |
    |
GitHub Actions

    |
    |
 Setup Python Environment

    |
    |
 Start PostgreSQL Service

    |
    |
 Install Dependencies

    |
    |
 Run pytest

    |
    |
 Pass / Fail
```


## Continuous Integration (CI)

Continuous Integration ensures that new code changes do not break the application.

The CI pipeline runs automatically when:

- Code is pushed to `main`
- A Pull Request is created targeting `main`

### CI Workflow

Current workflow file:

```
.github/workflows/ci.yml
```

Pipeline steps:

1. Checkout repository

2. Setup Python environment

3. Start PostgreSQL database service

4. Install application dependencies

5. Run automated tests

Example workflow:

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main


jobs:

  test:

    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: company
          POSTGRES_USER: admin
          POSTGRES_PASSWORD: password

        ports:
          - 5432:5432

        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:

      - name: Checkout code
        uses: actions/checkout@v4


      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"


      - name: Install dependencies
        run: |

          pip install -r app/requirements.txt


      - name: Run tests
        env:
          DATABASE_HOST: localhost
          DATABASE_PORT: 5432
          DATABASE_NAME: company
          DATABASE_USER: admin
          DATABASE_PASSWORD: password

        run: |

          pytest
```

## Test Database Configuration

GitHub Actions runs inside a fresh Ubuntu runner.

The runner does not contain:

- Local `.env` files
- Development databases
- Docker Compose networks


Therefore, CI creates a temporary PostgreSQL service container:

```
GitHub Runner

      |
      |
PostgreSQL 16 Container

      |
      |
FastAPI Tests
```

Database configuration is provided through environment variables:

```
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

Example:

```yaml
env:
  DATABASE_HOST: localhost
  DATABASE_PORT: 5432
  DATABASE_NAME: company
  DATABASE_USER: admin
  DATABASE_PASSWORD: password
```

## Pull Request Workflow

Development process:

```
Create Feature Branch

        |
        |
Commit Changes

        |
        |
Open Pull Request

        |
        |
GitHub Actions Runs

        |
        |
pytest Successful

        |
        |
Code Review

        |
        |
Merge main
```

Branch protection rules are configured to require:

- Successful CI checks
- Pull request review approval

## Docker Build Pipeline

### Current Status

Docker deployment is implemented using Docker Compose.

Current workflow:

```
Developer

    |
    |
Git Push

    |
    |
GitHub Actions

    |
    |
pytest

    |
    |
Merge
```


Docker image building is currently performed during deployment.

Future CI improvement:

```
pytest

   |
   |
docker build

   |
   |
Docker Image

   |
   |
Push Registry
```

Example future step:

```yaml
- name: Build Docker image

  run: |
    docker build \
    -t employee-api \
    ./app
```

## Deployment Pipeline

### Current Deployment

Application deployment is currently performed using:

- Docker Compose
- Nginx
- PostgreSQL
- Prometheus
- Grafana


Deployment flow:

```
Ubuntu Server

      |
      |
Docker Compose

      |
      |
Application Containers

      |
      |
Running Service
```

### Future Automated Deployment

Future CI/CD pipeline:

```
GitHub Actions

        |
        |
Docker Image Build

        |
        |
Container Registry

        |
        |
SSH Deployment

        |
        |
Production Server

        |
        |
Docker Compose Restart
```

Deployment steps:

1. Build Docker image
2. Push image to registry
3. Connect server using SSH key
4. Pull latest image
5. Restart containers

Example:

```bash
docker compose pull

docker compose up -d
```

## Secrets Management

Sensitive information should never be committed to Git.
Bad:

```env
DATABASE_PASSWORD=password
```

Better:

```
GitHub Secrets

       |
       |
GitHub Actions Environment

       |
       |
Application
```

Recommended secrets:

```
DATABASE_PASSWORD

SSH_PRIVATE_KEY

DOCKER_USERNAME

DOCKER_TOKEN
```

## Troubleshooting During Development

Common CI/CD issues documented:

- PostgreSQL hostname resolution failure
- Missing environment variables
- Python dependency compatibility
- Docker networking problems
- Container communication failures

Detailed troubleshooting:

```
docs/troubleshooting/
```

# Current Status

Completed:

- [x] GitHub Actions CI pipeline
- [x] Automated pytest execution
- [x] PostgreSQL service container
- [x] Pull request validation
- [x] Branch protection rules

Future improvements:

- [ ] Docker image build in CI
- [ ] Push image to GitHub Container Registry
- [ ] Automated server deployment
- [ ] HTTPS deployment
- [ ] Deployment rollback strategy
- [ ] Kubernetes deployment