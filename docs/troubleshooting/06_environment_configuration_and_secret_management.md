This is a good DevOps incident because it shows you understand:

* configuration management
* secrets management
* Git workflow
* Docker deployment practices
* development vs production differences

# Environment Configuration and Secret Management Problem

## Problem

During Docker deployment, the application required database configuration values.

The FastAPI application used environment variables:

```env
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

The first deployment attempt created a local `.env` file and used it directly.

However, this created a question:

- Should `.env` be uploaded to Git?
- Should secrets be stored inside Dockerfile?
- Should docker-compose.yml contain passwords?

---

# Environment

Project architecture:

```
Nginx
 |
 |
FastAPI Container
 |
 |
PostgreSQL Container
```

Project structure:

```
hoho-proj

├── app
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│
├── docker
│   └── docker-compose.yml
│
└── nginx
    └── nginx.conf
```

---

# Investigation

## Check Application Configuration

FastAPI loads database configuration through:

```
Environment Variables
        |
        |
        v
Pydantic Settings
        |
        |
        v
SQLAlchemy Database Connection
```

Example:

```python
class Settings(BaseSettings):

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
```

---

## Problem 1: Should `.env` be committed to Git?

Initial configuration:

```
app/.env
```

contains:

```env
DATABASE_HOST=postgres
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

This file contains sensitive information.

Committing it to Git creates a security risk.

Example:

```
Developer
    |
    |
    v
GitHub Repository
    |
    |
    v
Secret exposed
    |
    |
    v
Database compromise
```

---

# Root Cause

The deployment process mixed:

- application code
- environment configuration
- secrets

A production system should separate them.

Application code:

```
Git Repository
```

Configuration:

```
Deployment Environment
```

Secrets:

```
Secret Management System
```

---

# Solution

## Step 1: Create `.env.example`

Create:

```
app/.env.example
```

Content:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=change_me
```

Purpose:

- documents required variables
- allows new developers to configure the application
- contains no real secrets

---

## Step 2: Create local `.env`

Developers create:

```bash
cp app/.env.example app/.env
```

Then edit:

```bash
nano app/.env
```

Example:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

The local `.env` file is not committed.

---

## Step 3: Add `.env` to Git Ignore

Create:

```
.gitignore
```

Add:

```gitignore
# Environment files
.env
app/.env

# Python
__pycache__/
*.pyc

# Virtual environment
.venv/
```

Verification:

```bash
git status
```

The `.env` file should not appear.

---

# Dockerfile Configuration

## Incorrect approach

Do not store secrets inside Dockerfile:

```dockerfile
ENV DATABASE_PASSWORD=password
```

Reason:

Docker images can expose environment information.

Example:

```bash
docker inspect image_name
```

could reveal secrets.

---

## Correct approach

Dockerfile only contains application build instructions:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

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

Configuration is injected during deployment.

---

# Docker Compose Configuration

## Development Environment

Docker Compose loads local environment:

```yaml
services:

  app:

    env_file:
      - ../app/.env
```

Flow:

```
app/.env

     |
     |
     v

FastAPI Container

     |
     |
     v

Application Settings
```

---

# Production Environment

Production systems should not use local `.env` files.

Common solutions:

## Cloud Secret Management

Example:

```
AWS Secrets Manager
        |
        |
        v
Application Container
```

or:

```
Kubernetes Secret
        |
        |
        v
Pod Environment
```

---

# Final Project Structure

After improvement:

```
hoho-proj

├── .gitignore

├── app
│   ├── Dockerfile
│   ├── .env.example
│   ├── requirements.txt
│   └── main.py

├── docker
│   └── docker-compose.yml

├── nginx
│   └── nginx.conf

└── docs
    └── troubleshooting
        └── 06_environment_configuration_and_secret_management.md
```

---

# Verification

Check Docker deployment:

```bash
docker compose up -d
```

Check containers:

```bash
docker ps
```

Check application logs:

```bash
docker compose logs app
```

Test API:

```bash
curl http://localhost:8000/health
```

Expected:

```json
{
    "status": "ok"
}
```

---

# Key Lessons Learned

1. Never commit `.env` files containing secrets.

2. Use `.env.example` to document required configuration.

3. Dockerfile should build applications, not store secrets.

4. Docker Compose is responsible for injecting runtime configuration.

5. Development and production environments require different secret management strategies.

6. Configuration management is a critical part of reliable DevOps deployment.
````

This fits well after your previous troubleshooting docs:

```
docs/troubleshooting/

01_postgresql_hostname_resolution_failure.md
02_environment_variable_not_loaded.md
03_python_dependency_compatibility.md
04_docker_installation_ubuntu2604.md
05_docker_image_pull_connection_failure.md
06_environment_configuration_and_secret_management.md
```

The sequence tells a good DevOps story:

1. Linux setup
2. Docker installation
3. Image pulling/network problems
4. Application configuration problems
5. Secret management and deployment practices
6. Production thinking
