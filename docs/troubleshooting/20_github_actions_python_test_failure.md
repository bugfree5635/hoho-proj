# GitHub Actions Python Test Failure

## Problem

CI pipeline:

```

GitHub Actions
|
|
pytest

```

fails.

Example:

```

ModuleNotFoundError

DATABASE_HOST missing

```

## Cause

GitHub runner is a fresh machine.

It does not have:

- .env
- PostgreSQL
- Docker network
- local configuration


## Solution

Create CI environment variables:

Example:

```yaml
env:
  DATABASE_HOST: localhost
  DATABASE_PORT: 5432
  DATABASE_NAME: company
  DATABASE_USER: admin
  DATABASE_PASSWORD: password
```

Install dependencies:

```yaml
- name: Install dependencies
  run:
    pip install -r app/requirements.txt
```

Run tests:

```yaml
- name: Test
  run:
    pytest
```

## Lesson

CI environments are clean environments.

Never depend on your local machine state.
