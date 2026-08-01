# Troubleshooting Documentation

# 2. Environment Variable Not Loaded

## Problem

When starting the FastAPI application:

```bash
uvicorn app.main:app --reload
```

the application failed during startup.

Error:

```
pydantic_core._pydantic_core.ValidationError:

5 validation errors for Settings

DATABASE_HOST
Field required

DATABASE_PORT
Field required

DATABASE_NAME
Field required

DATABASE_USER
Field required

DATABASE_PASSWORD
Field required
```

The application could not start because database configuration was missing.

---

# Environment

Development environment:

```
Ubuntu Linux Host

 |
 |
FastAPI Application
 |
 |
Pydantic Settings
 |
 |
PostgreSQL Database
```

Project structure:

```
hoho-proj/

├── .env
│
├── app/
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   └── api/
│       └── employees.py
│
└── docs/
    └── troubleshooting/
```

---

# Configuration

The application uses Pydantic Settings.

`app/config/settings.py`

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str


    class Config:
        env_file = ".env"


settings = Settings()
```

The application expects these environment variables:

```env
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

---

# Investigation

## 1. Check environment file location

Command:

```bash
find . -name ".env"
```

Initial result:

```
./app/.env
```

The `.env` file was located inside the application directory.

---

## 2. Check application startup location

The application was started from:

```bash
cd ~/practice/hoho-proj

uvicorn app.main:app --reload
```

The current working directory was:

```
~/practice/hoho-proj
```

Pydantic searched for:

```
~/practice/hoho-proj/.env
```

but the file existed at:

```
~/practice/hoho-proj/app/.env
```

---

# Root Cause Analysis

The application configuration depended on:

- current working directory
- `.env` file location
- environment variable names

The application was started from the project root, but the configuration file was stored inside the application folder.

Therefore:

```
FastAPI
 |
 |
Pydantic Settings
 |
 |
.env
```

failed because the expected configuration file was missing.

---

# Solution

## Move .env to project root

Before:

```
hoho-proj/

└── app/
    ├── .env
    ├── main.py
    └── config/
        └── settings.py
```

After:

```
hoho-proj/

├── .env
│
└── app/
    ├── main.py
    └── config/
        └── settings.py
```

Command:

```bash
mv app/.env .env
```

---

# Verify .env Content

`.env`

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

Important:

Correct:

```env
DATABASE_HOST=localhost
```

Incorrect:

```env
DATABASE_HOST = localhost
```

---

# Testing Configuration Loading

From project root:

```bash
cd ~/practice/hoho-proj
```

Start Python:

```bash
python
```

Test:

```python
from config.settings import settings

print(settings.DATABASE_HOST)
```

Expected output:

```
localhost
```

---

# Start Application

Run:

```bash
uvicorn app.main:app --reload
```

Successful result:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

# Production Consideration

In production environments, configuration should not be stored inside source code.

Common approaches:

## Docker Compose

Example:

```yaml
services:

  api:
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_NAME: company
      DATABASE_USER: admin
```

---

## Environment Management Tools

Common solutions:

- Docker secrets
- Kubernetes ConfigMap
- Kubernetes Secrets
- HashiCorp Vault
- Cloud provider secret managers

---

# Key Lessons Learned

1. Application configuration should be separated from application code.

2. Environment variables depend on:

   - application startup directory
   - deployment method
   - configuration loading mechanism

3. Debug configuration problems by checking:

   - Is the `.env` file present?
   - Is the filename correct?
   - Are variable names matching?
   - Is the application reading the correct path?

4. Local development and production environments usually manage configuration differently.

---

# Skills Demonstrated

- Python application configuration management
- Pydantic Settings
- Environment variable debugging
- Linux file structure understanding
- Deployment troubleshooting
- Production configuration concepts