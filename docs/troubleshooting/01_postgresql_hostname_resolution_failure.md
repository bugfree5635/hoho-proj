# Troubleshooting Documentation

## 1. PostgreSQL Hostname Resolution Failure

### Problem

When starting the FastAPI application:

```bash
uvicorn main:app --reload
```

the application failed with:

```
psycopg.OperationalError:
failed to resolve host 'postgres':
[Errno -3] Temporary failure in name resolution
```

The application could not connect to PostgreSQL.

---

## Environment

Development environment:

```
Ubuntu Host
 |
 |
FastAPI application
 |
 |
SQLAlchemy
 |
 |
PostgreSQL Docker Container
```

Configuration:

`.env`

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
```

---

## Root Cause Analysis

The hostname:

```
postgres
```

is a Docker Compose service name.

Docker provides internal DNS resolution:

```
FastAPI container
        |
        |
        postgres
        |
        |
PostgreSQL container
```

However, FastAPI was running directly on the Ubuntu host:

```
Ubuntu
 |
 |
FastAPI
```

The Ubuntu system DNS does not know:

```
postgres = PostgreSQL container IP
```

Therefore the hostname resolution failed.

---

## Solution

### Development Solution

Run PostgreSQL inside Docker but expose the port to localhost.

Docker:

```bash
docker run \
--name postgres \
-e POSTGRES_DB=company \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=password \
-p 5432:5432 \
-d postgres:16
```

Change `.env`:

Before:

```env
DATABASE_HOST=postgres
```

After:

```env
DATABASE_HOST=localhost
```

Now the connection becomes:

```
FastAPI
 |
localhost:5432
 |
PostgreSQL Container
```

---

## Production Solution

For production deployment, run FastAPI and PostgreSQL together using Docker Compose.

Example:

```
Docker Network

FastAPI Container
        |
        |
postgres
        |
        |
PostgreSQL Container
```

In this environment:

```env
DATABASE_HOST=postgres
```

is correct because Docker DNS resolves the service name.

---

## Verification

Check PostgreSQL container:

```bash
docker ps
```

Test database connection:

```bash
psql -h localhost -U admin -d company
```

Restart application:

```bash
uvicorn main:app --reload
```

API became available:

```
http://localhost:8000/docs
```

---

## Key Lessons Learned

1. Docker service names only work inside Docker networks.

2. Host machines and containers have different network namespaces.

3. Database connection problems are often caused by:

   * wrong hostname
   * wrong port
   * container not running
   * network configuration

4. Always check the environment where the application is running before debugging the application code.

---

## Also update your `02_application_deployment.md`

Do not put the whole error there. Add only a reference:

## Troubleshooting

During deployment, I encountered a PostgreSQL hostname resolution issue caused by running FastAPI outside the Docker network.

Detailed analysis:
See:
docs/troubleshooting.md

sudo tee /etc/docker/daemon.json <<-'EOF'
{                                         
    "registry-mirrors": [
     "https://docker.1ms.run",
     "https://dockerproxy.link",
     "https://docker.m.daocloud.io",
     "https://docker.jiaxin.site",
     "https://docker.xuanyuan.me",
     "https://registry.cyou",
     "https://free.hubfast.cn",
     "https://mirror.ccs.tencentyun.com"
    ]
}
EOF

sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf <<-'EOF'
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7897"
Environment="HTTPS_PROXY=http://127.0.0.1:7897"
EOF

export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890


[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"