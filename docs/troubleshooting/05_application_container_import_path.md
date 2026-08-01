# 05 Application Container Import Path Troubleshooting

## Problem

The FastAPI application worked locally but failed after Docker deployment.

The container failed during startup with:

```
ModuleNotFoundError: No module named 'app'
```

Example error:

```text
File "/app/main.py"

from app.database.connection import engine

ModuleNotFoundError: No module named 'app'
```

---

# Environment

Project structure before fixing:

```
hoho-proj

├── app
│   ├── main.py
│   ├── database
│   ├── api
│   ├── config
│   ├── requirements.txt
│   └── Dockerfile
│
└── docker
    └── docker-compose.yml
```

The Docker build context was:

```yaml
build:
  context: ../app
```

Therefore Docker copied the content inside `app`:

Container filesystem:

```
/app

├── main.py
├── database
├── api
├── config
└── requirements.txt
```

There was no:

```
/app/app
```

directory.

---

# Root Cause Analysis

The application used package-style imports:

```python
from app.database.connection import engine
from app.database.models import Base
from app.api.employees import router
```

Python expected:

```
app
 |
 ├── database
 |
 ├── api
 |
 └── config
```

However Docker created:

```
/app

├── main.py
├── database
├── api
└── config
```

The package name `app` no longer existed.

The problem was caused by the difference between:

* local project directory
* Docker container filesystem
* Python import path

---

# Solution

Remove the `app.` prefix from Python imports.

Before:

```python
from app.database.connection import engine
from app.database.models import Base
from app.api.employees import router
```

After:

```python
from database.connection import engine
from database.models import Base
from api.employees import router
```

---

# Updated Dockerfile

The final Dockerfile:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [
"uvicorn",
"main:app",
"--host",
"0.0.0.0",
"--port",
"8000"
]
```

---

# Updated Container Layout

After rebuilding:

```
FastAPI Container

/app

├── main.py
├── database
│   ├── connection.py
│   └── models.py
│
├── api
│   └── employees.py
│
├── config
│   └── settings.py
│
└── requirements.txt
```

Uvicorn starts:

```
main:app
```

meaning:

```
main.py

app = FastAPI()
```

---

# Verification

Rebuild the image:

```bash
docker compose build --no-cache
```

Start services:

```bash
docker compose up -d
```

Check application logs:

```bash
docker compose logs app
```

Expected:

```
Application startup complete.

Uvicorn running on http://0.0.0.0:8000
```

---

Check API health:

```bash
curl localhost/health
```

Expected:

```json
{
    "status": "ok"
}
```

Swagger documentation:

```
http://localhost/docs
```

---

# Lessons Learned

1. Docker changes the filesystem structure inside containers.

2. Python imports must match the runtime directory structure.

3. `WORKDIR`, `COPY`, and `uvicorn module:app` are tightly connected.

4. When debugging container startup problems:

```
Check logs
    |
Check filesystem
    |
Check Python imports
    |
Check environment variables
    |
Restart container
```

5. A clean Docker image should have a simple application entry point:

```
uvicorn main:app
```

instead of unnecessary package nesting.

---

# Final Architecture

```
Browser

   |
   |

Nginx Container

   |
   |

FastAPI Container

   |
   |

PostgreSQL Container
```

The deployment is now working correctly.

Your current structure is actually closer to many small production services. Many teams do **not** force a top-level package name when the service itself is already isolated in its own container. The important thing is consistency between:

```
Dockerfile
        |
        |
WORKDIR
        |
        |
COPY
        |
        |
Python imports
        |
        |
uvicorn main:app
```

Now your next real DevOps step is probably adding **Docker healthcheck + depends_on condition + Nginx upstream troubleshooting**, because that is where real deployments usually fail.
