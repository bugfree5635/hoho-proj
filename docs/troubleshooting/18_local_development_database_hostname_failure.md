# Local Development Database Hostname Failure

## Problem

Running:

```bash
uvicorn app.main:app --reload
```

Error:

```
failed to resolve host 'postgres'
```

Example:

```
psycopg.OperationalError:
failed to resolve host 'postgres'
```

## Cause

Docker DNS provides service names:

```
postgres
```

only inside Docker network.

Example:

```
FastAPI container

        |
        |
 Docker DNS

        |
        
postgres container
```

But local machine:

```
Ubuntu host

 |
 |
postgres
```

has no DNS record.

## Solution

When running locally:

Use:

```
DATABASE_HOST=localhost
```

Example:

```
DATABASE_HOST=127.0.0.1
```

When running inside Docker:

Use:

```
DATABASE_HOST=postgres
```

## Lesson

Same application has different database addresses:

Docker:

```
postgres
```

Local:

```
localhost
```

Environment configuration must match execution environment.

