For your **Linux Infrastructure Project**, the Python application part should not be a random toy app. It should simulate a real internal company service that a sysadmin/DevOps engineer would deploy and maintain.

I recommend:

# Python Application: Employee Management REST API

Architecture:

```text
Client
  |
HTTP Request
  |
Nginx Reverse Proxy
  |
Docker Container
  |
FastAPI Application
  |
SQLAlchemy ORM
  |
PostgreSQL Database
```

---

# 1. REST API

## Goal

Build an API service that allows users to manage employees.

Example:

### Create employee

Request:

```
POST /employees
```

Body:

```json
{
    "name": "Henry",
    "email": "henry@example.com",
    "department": "IT"
}
```

Response:

```json
{
    "id": 1,
    "name": "Henry",
    "email": "henry@example.com",
    "department": "IT"
}
```

---

## API endpoints

### Health check

Important for monitoring:

```
GET /health
```

Response:

```json
{
    "status": "ok"
}
```

Why?

Your monitoring system can check:

```
Prometheus
      |
      |
 /health endpoint
```

---

### Employee API

| Method | Endpoint          | Function         |
| ------ | ----------------- | ---------------- |
| GET    | `/employees`      | list employees   |
| GET    | `/employees/{id}` | get one employee |
| POST   | `/employees`      | create employee  |
| PUT    | `/employees/{id}` | update employee  |
| DELETE | `/employees/{id}` | delete employee  |

---

# 2. Configuration Management

Do not put settings directly inside code.

Bad:

```python
DATABASE_PASSWORD="123456"
```

Good:

```
Application

     |

Environment variables

     |

.env file

     |

Database
```

Example:

`.env`

```bash
APP_NAME=employee-api

DB_HOST=postgres

DB_PORT=5432

DB_NAME=company

DB_USER=admin

DB_PASSWORD=password
```

---

Python reads:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    app_name: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


settings = Settings()
```

Now the same application can run in:

Development:

```
Laptop
```

Production:

```
Docker Server
```

without changing code.

---

# 3. Database Connection

Use:

```
FastAPI

 |

SQLAlchemy

 |

PostgreSQL
```

Example database table:

```
employees

+----+-------+-------------------+
| id | name  | email             |
+----+-------+-------------------+
| 1  | Henry | henry@test.com    |
+----+-------+-------------------+
```

---

Model:

```python
class Employee(Base):

    __tablename__ = "employees"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String
    )


    email = Column(
        String,
        unique=True
    )


    department = Column(
        String
    )
```

---

# Project structure

Your GitHub:

```
app/

├── main.py

├── requirements.txt

├── Dockerfile

├── .env.example

├── config/
│   └── settings.py

├── database/
│   ├── connection.py
│   └── models.py

├── api/
│   └── employees.py

├── schemas/
│   └── employee.py

└── tests/
    └── test_api.py
```

---

# Docker deployment

Your final infrastructure:

```
docker-compose.yml


services:

  api:
    build:
      .
    ports:
      - "8000:8000"


  postgres:
    image:
      postgres:16


  nginx:
    image:
      nginx
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

Logs:

```bash
docker logs api
```

---

# Sysadmin troubleshooting scenarios

You should intentionally practice:

## Problem 1

API cannot connect database.

You check:

```bash
docker logs api

docker logs postgres

docker network ls
```

---

## Problem 2

Nginx returns:

```
502 Bad Gateway
```

You check:

```bash
systemctl status nginx

curl localhost:8000

docker ps
```

---

## Problem 3

Database disk full.

You check:

```bash
df -h

du -sh /var/lib/docker
```

---

# What this project proves in an interview

You can say:

> "I developed and deployed a containerized Python REST API. I configured application settings using environment variables, connected the service to PostgreSQL, deployed it behind Nginx, and monitored its health."

This connects:

**Python + Linux + Docker + Nginx + Database + Operations**

which is exactly the bridge from **Sysadmin → DevOps**.
