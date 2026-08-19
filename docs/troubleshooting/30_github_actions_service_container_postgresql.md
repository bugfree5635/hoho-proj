# GitHub Actions Service Container PostgreSQL

## Problem

GitHub Actions tests that require PostgreSQL fail because the workflow cannot connect to the database.

Typical errors include:

```text
connection refused
```

or:

```text
could not translate host name "postgres"
```

or:

```text
connection to server at "localhost", port 5432 failed
```

The tests may work locally:

```bash
pytest
```

but fail in GitHub Actions.

## Cause

GitHub Actions runs the CI job in an isolated environment.

Your local PostgreSQL:

```text
Your computer
    ↓
PostgreSQL
    ↓
localhost:5432
```

does not automatically exist inside GitHub Actions.

A PostgreSQL service container needs to be explicitly configured in the workflow.

## Solution

Add PostgreSQL as a GitHub Actions service:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U postgres -d test_db"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"

      - name: Install dependencies
        run: |
          pip install -r app/requirements.txt
          pip install -r app/requirements-dev.txt

      - name: Run migrations
        env:
          DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/test_db
        run: alembic upgrade head

      - name: Run tests
        env:
          DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/test_db
        run: pytest
```

## Database Host

The correct database hostname depends on how the GitHub Actions job is configured.

### Job running directly on the GitHub runner

If your workflow uses:

```yaml
runs-on: ubuntu-latest
```

and PostgreSQL is configured as a service with:

```yaml
ports:
  - 5432:5432
```

the application can connect through:

```text
localhost:5432
```

For example:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/test_db
```

### Job running inside a container

If the job itself runs inside a container, service-container networking is different.

For example:

```yaml
container:
  image: python:3.14
```

Then the PostgreSQL service can normally be reached using its service name:

```text
postgres
```

rather than:

```text
localhost
```

For example:

```text
postgresql+psycopg://postgres:postgres@postgres:5432/test_db
```

This distinction is important:

```text
Runner job:

application
    ↓
localhost:5432
    ↓
PostgreSQL service


Container job:

application container
    ↓
postgres:5432
    ↓
PostgreSQL service
```

## Debug

First check the PostgreSQL service configuration:

```yaml
services:
  postgres:
    image: postgres:16
```

Then check the environment variables:

```yaml
env:
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  POSTGRES_DB: test_db
```

Make sure your application uses the same values.

For example:

```text
POSTGRES_DB=test_db
```

must correspond to:

```text
postgresql+psycopg://postgres:postgres@...:5432/test_db
```

## Check PostgreSQL Health

Use a health check:

```yaml
options: >-
  --health-cmd="pg_isready -U postgres -d test_db"
  --health-interval=10s
  --health-timeout=5s
  --health-retries=5
```

This helps prevent tests from starting before PostgreSQL is ready.

The important difference is:

```text
Container started
        ≠
Database ready
```

PostgreSQL may have started its container while still initializing the database.

## Check the Connection

Add a temporary debugging step:

```yaml
- name: Check PostgreSQL
  env:
    PGPASSWORD: postgres
  run: |
    pg_isready -h localhost -p 5432 -U postgres -d test_db
```

If `psql` is available:

```bash
PGPASSWORD=postgres \
psql -h localhost -U postgres -d test_db -c "SELECT 1;"
```

You can also test the connection from Python:

```bash
python -c "
import psycopg
conn = psycopg.connect(
    'postgresql://postgres:postgres@localhost:5432/test_db'
)
print('PostgreSQL connection OK')
conn.close()
"
```

## Environment Variable Problem

A common mistake is having different database URLs locally and in CI.

For example, local:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/hoho
```

but CI:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/test_db
```

This is not necessarily wrong.

The important thing is that the hostname and database match the environment.

A good approach is to configure the database through an environment variable:

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

Then:

```text
Local development
        ↓
localhost

GitHub Actions
        ↓
localhost or postgres

Production
        ↓
production database hostname
```

The application code does not need to change.

## Alembic

If your tests use a database schema, run migrations before running tests:

```yaml
- name: Run migrations
  env:
    DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/test_db
  run: alembic upgrade head
```

Then:

```yaml
- name: Run tests
  env:
    DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/test_db
  run: pytest
```

The order matters:

```text
Start PostgreSQL
      ↓
Wait for PostgreSQL
      ↓
alembic upgrade head
      ↓
Create database schema
      ↓
pytest
```

Without the migration step, tests may fail with:

```text
relation "users" does not exist
```

or:

```text
relation "employees" does not exist
```

## Common Mistake: Using Docker Compose

If your local project has:

```yaml
services:
  postgres:
    image: postgres:16

  fastapi:
    ...
```

you do not automatically get the same Compose network inside GitHub Actions.

GitHub Actions service containers are configured in:

```yaml
jobs:
  test:
    services:
      postgres:
```

You can use Docker Compose in CI if you want, but it is often simpler for unit/API tests to use GitHub Actions' built-in service-container mechanism.

## Common Mistake: `localhost` vs `postgres`

This is one of the most important things to understand.

### GitHub runner job

```yaml
runs-on: ubuntu-latest
```

with:

```yaml
ports:
  - 5432:5432
```

usually uses:

```text
localhost:5432
```

### Containerized job

```yaml
container:
  image: python:3.14
```

usually communicates with the service using:

```text
postgres:5432
```

Do not blindly copy:

```text
postgres
```

from your Docker Compose configuration into a normal GitHub runner job.

## Verify

A successful CI flow should look like:

```text
GitHub Actions
      ↓
Start PostgreSQL service
      ↓
PostgreSQL health check
      ↓
Install Python dependencies
      ↓
Set DATABASE_URL
      ↓
alembic upgrade head
      ↓
pytest
      ↓
coverage
      ↓
success
```

Example:

```yaml
- name: Run migrations
  env:
    DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/test_db
  run: alembic upgrade head

- name: Run tests
  env:
    DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/test_db
  run: pytest --cov=app --cov-fail-under=80
```

## Lesson

A CI database is a separate environment from your local database.

The important concepts are:

```text
Local PostgreSQL
       ≠
GitHub Actions PostgreSQL
       ≠
Production PostgreSQL
```

Your application should therefore obtain its database connection from configuration rather than hard-coding a hostname.

The key lesson is:

> **When using PostgreSQL in GitHub Actions, explicitly create the database service, wait until it is healthy, configure the correct hostname, run migrations, and only then run tests.**
