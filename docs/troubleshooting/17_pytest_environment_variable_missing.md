# Pytest Environment Variable Missing

## Problem

Running:

```bash
pytest
```

Error:

```
pydantic_core.ValidationError

DATABASE_HOST
Field required

DATABASE_PORT
Field required
```

## Cause

The application loads configuration:

```python
settings = Settings()
```

from environment variables.

Production Docker uses:

```
.env
```

but local pytest does not automatically load it.

Docker:

```
docker-compose.yml

env_file:
  - .env
```

works.

Local:

```
pytest
```

does not.

## Solution 1

Export variables:

```bash
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=company
export DATABASE_USER=admin
export DATABASE_PASSWORD=password
```

Then:

```bash
pytest
```

## Solution 2

Create:

```
.env
```

inside project:

```
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

## Lesson

Container environments and local development environments are different.

Always define how developers run the application locally.

