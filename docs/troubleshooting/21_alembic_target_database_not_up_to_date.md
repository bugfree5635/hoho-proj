# Alembic Target Database Not Up to Date

## Problem

When generating a new migration:

```bash
alembic revision --autogenerate -m "add users table"
```

Alembic returns:

```text
ERROR [alembic.util.messaging] Target database is not up to date.
FAILED: Target database is not up to date.
```

## Cause

The PostgreSQL database has not applied the latest existing Alembic migration.

For example:

```text
Migration files:

001_initial
002_add_users   ← latest

Database:

001_initial      ← current
```

Alembic expects the database to be at the current migration head before generating another migration.

## Debug

Check the current database revision:

```bash
alembic current
```

Check the migration history:

```bash
alembic history
```

Check the latest migration:

```bash
alembic heads
```

If the database is behind the migration head, upgrade it:

```bash
alembic upgrade head
```

## Solution

Run:

```bash
alembic upgrade head
```

Then generate the new migration:

```bash
alembic revision --autogenerate -m "add users table"
```

The normal workflow is:

```text
Modify SQLAlchemy models
        ↓
alembic upgrade head
        ↓
alembic revision --autogenerate
        ↓
Review migration
        ↓
alembic upgrade head
```

When using Docker, make sure Alembic is connecting to the PostgreSQL container using the Docker service hostname, for example:

```text
postgres-db:5432
```

rather than `localhost:5432`.

## Verify

Run:

```bash
alembic current
```

Then:

```bash
alembic heads
```

The current database revision should match the migration head.

You can also check the database:

```bash
alembic upgrade head
```

If there is no output indicating a migration is being applied, the database is already at the latest revision.

## Lesson

Alembic has two important pieces of state:

```text
alembic/versions/
        ↓
Migration history in the project

PostgreSQL
        ↓
alembic_version
        ↓
Currently applied migration
```

`alembic revision --autogenerate` should normally be run when the database is already at the current migration head.

The key lesson is:

> **Migration files and the database migration state must stay synchronized.**
