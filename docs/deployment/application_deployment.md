# Module 02: Application Deployment

## Objective

Deploy a complete web application infrastructure similar to a real production environment.

The goal of this module is to practice:

- Application deployment
- Docker container management
- Database integration
- Reverse proxy configuration
- Service networking
- Troubleshooting production problems


---

# 1. Architecture


```
                Client
                  |
                  |
              Port 80
                  |
                  |
             Nginx Proxy
                  |
                  |
          Docker Network
                  |
      +-----------+-----------+
      |                       |
      |                       |

FastAPI Container       PostgreSQL Container
|
|
SQLAlchemy
|
|
PostgreSQL Database

```


Components:


| Component | Purpose |
|---|---|
| Nginx | Reverse proxy and HTTP gateway |
| FastAPI | Backend REST API application |
| PostgreSQL | Application database |
| Docker | Container management |
| Docker Network | Service communication |



---

# 2. Project Structure


```

hoho-proj

├── app
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── api
│   ├── database
│   ├── config
│   └── tests
│
├── docker
│   └── docker-compose.yml
│
├── nginx
│   └── nginx.conf
│
└── docs
└── deployment

```

---

# 3. Environment Preparation


## Requirements


Install:


- Docker
- Docker Compose
- Python 3.14
- Git


Check Docker:


```bash
docker --version
Docker version 29.1.3
```

Check Docker Compose:

```bash
docker compose version
Docker Compose version 2.40.3
```

## Docker Environment

The application deployment environment uses:

- Ubuntu 26.04
- Docker Engine 29.1.3
- Docker Compose 2.40.3

Docker installation troubleshooting:

See:

docs/troubleshooting/04_docker_installation_ubuntu2604.md

---

# 4. Python Application Deployment

## Application Features

The FastAPI application provides:

* REST API
* Configuration management
* Database connection
* Employee management API

Application entry:

```
app/main.py
```

Example:

```python
app = FastAPI(
    title="Employee Management API",
    version="1.0"
)
```

---

# 5. Application Dockerfile

Location:

```
app/Dockerfile
```

Content:

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

## Explanation

`WORKDIR`

Defines application directory inside container.

`COPY requirements.txt`

Copies dependency list.

`pip install`

Installs Python packages.

`CMD`

Starts FastAPI server.

---

# 6. Docker Compose Deployment

Location:

```
docker/docker-compose.yml
```

Example:

```yaml
services:

  app:

    build:

      context: ../app


    container_name: fastapi-app


    env_file:

      - ../app/.env


    expose:

      - "8000"


    networks:

      - backend



  postgres:


    image: postgres:16


    container_name: postgres-db


    environment:

      POSTGRES_DB: company

      POSTGRES_USER: admin

      POSTGRES_PASSWORD: password


    volumes:

      - postgres_data:/var/lib/postgresql/data


    networks:

      - backend




  nginx:


    image: nginx:latest


    container_name: nginx-proxy


    ports:

      - "80:80"


    volumes:

      - ../nginx/nginx.conf:/etc/nginx/nginx.conf


    depends_on:

      - app


    networks:

      - backend




volumes:


  postgres_data:



networks:


  backend:
```

---

# 7. Docker Networking

Docker creates an internal network:

```
Docker Network


fastapi-app

     |

     |

postgres-db

```

Containers communicate using service names.

Example:

```
DATABASE_HOST=postgres
```

Docker DNS automatically resolves:

```
postgres

        |

        |

PostgreSQL container IP
```

---

# 8. Database Configuration

Environment file:

```
app/.env
```

Example:

```env
DATABASE_HOST=postgres

DATABASE_PORT=5432

DATABASE_NAME=company

DATABASE_USER=admin

DATABASE_PASSWORD=password
```

---

# 9. Nginx Configuration

Location:

```
nginx/nginx.conf
```

Configuration:

```nginx
events {}


http {


upstream fastapi_backend {


    server app:8000;


}



server {


    listen 80;



    location / {


        proxy_pass http://fastapi_backend;



        proxy_set_header Host $host;


        proxy_set_header X-Real-IP $remote_addr;


    }



}


}
```

---

# 10. Deployment Process

## Step 1: Go to Docker directory

```bash
cd docker
```

---

## Step 2: Build images

```bash
docker compose build
```

Docker will:

1. Build FastAPI image
2. Download PostgreSQL image
3. Download Nginx image

---

## Step 3: Start services

```bash
docker compose up
```

Run in background:

```bash
docker compose up -d
```

---

## Step 4: Verify containers

```bash
docker ps
```

Expected:

```
nginx-proxy

fastapi-app

postgres-db
```

---

# 11. Application Testing

## Health Check

Request:

```
GET /health
```

Command:

```bash
curl http://localhost/health
```

Response:

```json
{
 "status":"ok"
}
```

---

# 12. API Testing

## Create Employee

Endpoint:

```
POST /employees
```

Example:

```bash
curl -X POST http://localhost/employees \
-H "Content-Type: application/json" \
-d '
{
"name":"Henry",
"email":"henry@test.com",
"department":"IT"
}
'
```

Response:

```json
{
"id":1,
"name":"Henry",
"email":"henry@test.com",
"department":"IT"
}
```

---

# 13. Troubleshooting

## Problem 1: 502 Bad Gateway

## Symptom

Browser shows:

```
502 Bad Gateway
```

---

## Investigation

Check Nginx:

```bash
docker logs nginx-proxy
```

Check application:

```bash
docker logs fastapi-app
```

Check containers:

```bash
docker ps
```

---

## Possible Causes

### Application container stopped

Check:

```bash
docker ps -a
```

Restart:

```bash
docker start fastapi-app
```

---

### Wrong upstream configuration

Wrong:

```nginx
server localhost:8000;
```

Correct:

```nginx
server app:8000;
```

Because Nginx runs inside Docker network.

---

# Problem 2: PostgreSQL Connection Failure

## Error

```
failed to resolve host 'postgres'
```

---

## Cause

FastAPI was running on the Ubuntu host.

The hostname:

```
postgres
```

only exists inside Docker network.

Host machine cannot resolve Docker DNS.

---

## Solution 1: Local Development

Run PostgreSQL:

```bash
docker run \
--name postgres \
-e POSTGRES_DB=company \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=password \
-p 5432:5432 \
-d postgres:16
```

Change:

Before:

```env
DATABASE_HOST=postgres
```

After:

```env
DATABASE_HOST=localhost
```

---

## Solution 2: Production

Run FastAPI and PostgreSQL together with Docker Compose.

Then:

```env
DATABASE_HOST=postgres
```

works because Docker DNS resolves service names.

---

# Problem 3: Container Crash

## Symptom

Container exits immediately.

Check:

```bash
docker ps -a
```

View logs:

```bash
docker logs fastapi-app
```

Common causes:

* Missing environment variables
* Python dependency errors
* Application startup failure

---

# Problem 4: Environment Variable Not Loaded

## Error

```
ValidationError:
DATABASE_HOST field required
```

---

## Investigation

Check:

```bash
cat app/.env
```

Verify:

```env
DATABASE_HOST
DATABASE_USER
DATABASE_PASSWORD
```

Restart:

```bash
docker compose restart
```

---

# Problem 5: Port Already Used

## Error

```
bind: address already in use
```

Check:

```bash
sudo lsof -i :8000
```

Kill process:

```bash
kill PID
```

---

# 14. Operational Commands

View logs:

```bash
docker logs container_name
```

Enter container:

```bash
docker exec -it container_name bash
```

Restart service:

```bash
docker restart container_name
```

Stop deployment:

```bash
docker compose down
```

---

# 15. Lessons Learned

## Docker

Learned:

* Image building
* Container lifecycle
* Volumes
* Networks
* Service discovery

---

## Linux Administration

Learned:

* Service troubleshooting
* Log analysis
* Port checking
* Configuration management

---

## Networking

Learned:

* Reverse proxy
* Internal DNS
* Container networking
* Port mapping

---

## DevOps Practice

Learned:

* Deploy applications
* Monitor failures
* Debug production-like problems
* Document incidents

---

# Final Result

This module demonstrates ability to deploy and operate:

```
Production-like Web Service


Nginx

  |

FastAPI

  |

PostgreSQL

  |

Docker Infrastructure

```

Skills demonstrated:

* Linux administration
* Docker
* Application deployment
* Database operations
* Networking troubleshooting
* Infrastructure documentation

```

This document fits your portfolio because it shows not only "I built an app", but **"I can deploy, operate, and troubleshoot a service"**, which is what SysAdmin/DevOps recruiters look for.
```
