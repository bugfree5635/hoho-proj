# GitHub Actions Pipeline

## Purpose

GitHub Actions is used to automatically validate code changes before they are merged into the main branch.

The current implementation focuses on **Continuous Integration (CI)**:

- Installing dependencies
- Starting test services
- Running automated tests
- Validating application changes

Future improvements will extend the pipeline into **Continuous Deployment (CD)**.

## Workflow Location

GitHub Actions workflows are stored in:

```
.github/

└── workflows/
    └── ci.yml
```

## Pipeline Flow

```
Developer

    |
    |
Push code / Create Pull Request

    |
    |
GitHub Actions Trigger

    |
    |
Checkout Repository

    |
    |
Setup Python Environment

    |
    |
Start PostgreSQL Test Database

    |
    |
Install Dependencies

    |
    |
Run pytest

    |
    |
CI Result

    |
    |
Merge Allowed
```

## Workflow Trigger

The pipeline runs on:

### Push

```yaml
push:
  branches:
    - main
```

When code is pushed to the main branch.

### Pull Request

```yaml
pull_request:
  branches:
    - main
```

When a pull request targets the main branch.

## Runner

Current runner:

```
ubuntu-latest
```


GitHub provides temporary virtual machines called runners.

The runner:

- Starts when workflow begins
- Executes jobs
- Is destroyed after completion

Example:

```
GitHub Server

      |
      |
Temporary Ubuntu Runner

      |
      |
Run Tests

      |
      |
Runner Deleted
```

## Why ubuntu-latest?

`ubuntu-latest` is recommended for most CI workloads because:

- Maintained by GitHub
- Receives security updates
- Provides a stable environment
- Automatically upgrades to newer supported Ubuntu versions

Using a fixed version like:

```
ubuntu-26.04
```

is not recommended unless that image is officially supported by GitHub Actions.

## CI Job

Current job:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

Job name:

```
test
```

GitHub displays the check as:

```
CI Pipeline / test
```

This check is required by branch protection rules before merging.

## PostgreSQL Test Service

The application requires PostgreSQL.

The GitHub runner does not contain the project database.

Therefore, the workflow creates a temporary PostgreSQL container:

```
GitHub Runner

      |
      |
PostgreSQL 16 Service

      |
      |
FastAPI Application Tests
```

Configuration:

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_DB: company
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
```

## Pull Request Protection

The repository uses branch protection rules:

Required:

- Pull request review approval
- Successful GitHub Actions checks

Workflow:

```
Create Branch

      |
      |
Commit Changes

      |
      |
Open Pull Request

      |
      |
CI Pipeline Runs

      |
      |
pytest Passed

      |
      |
Code Review

      |
      |
Merge main
```


## Failure Handling

If tests fail:

```
Code Change

      |
      |
GitHub Actions

      |
      |
pytest Failed

      |
      |
Merge Blocked
```

This prevents broken code from entering the main branch.

## Current Pipeline Status

Implemented:

- [x] GitHub Actions workflow
- [x] Python environment setup
- [x] Dependency installation
- [x] PostgreSQL test database
- [x] Automated pytest execution
- [x] Pull request validation
- [x] Branch protection rules

## Future CD Pipeline

The next step is adding Continuous Deployment.

Future flow:

```
GitHub Actions

        |
        |
Run Tests

        |
        |
Build Docker Image

        |
        |
Push Image Registry

        |
        |
SSH Into Server

        |
        |
Update Docker Compose

        |
        |
Application Running
```

Future improvements:

- Docker image publishing
- Automated server deployment
- HTTPS configuration
- Deployment rollback
- Kubernetes deployment