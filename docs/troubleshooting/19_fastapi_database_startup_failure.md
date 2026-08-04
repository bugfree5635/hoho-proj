# FastAPI Database Startup Failure

## Problem

FastAPI cannot start.

Error:

```

Base.metadata.create_all(bind=engine)

```

fails during startup.

Example:

```

sqlalchemy.exc.OperationalError

```

## Cause

Application creates database tables during startup:

```python
Base.metadata.create_all(bind=engine)
```

If PostgreSQL is unavailable:

```
FastAPI startup
        |
        |
SQLAlchemy
        |
        |
PostgreSQL
```

startup fails.

## Debug

Check PostgreSQL:

```bash
docker ps
```

Check logs:

```bash
docker logs postgres-db
```

Check network:

```bash
docker network inspect docker_backend
```

## Solution

Start database first:

```bash
docker compose up postgres
```

or:

```bash
docker compose up -d
```

## Improvement

Production systems usually use:

* database migration tools
* health checks
* retry mechanisms

Example:

```
FastAPI
 |
wait until database ready
 |
start service
```

## Lesson

Application startup depends on external services.

