# Accessing Application from Host Machine

## Problem

After deploying the application with Docker inside Ubuntu VMware, accessing:

```
http://localhost/
```

did not open the FastAPI application.

Instead, the browser showed:

```

HTTP Error 404.0 - Not Found

Module: IIS Web Core
Handler: StaticFile

Physical Path:
C:\inetpub\wwwroot\health

```

This indicated the request was handled by Windows IIS, not Docker Nginx.

---

# Environment

Deployment architecture:

```

Windows Host
|
|
VMware Ubuntu
|
|
Docker
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

The application was running inside the Ubuntu VM.

---

# Root Cause

## localhost points to the current machine

When opening:

```
http://localhost/
```

from Windows browser:

```

localhost
|
v
Windows Host

```

The request went to Windows services.

In this case:

```

Windows IIS
|
|
C:\inetpub\wwwroot

```

was responding.

The request never reached:

```

Ubuntu VM
|
Docker Nginx

```

---

# Diagnosis

## Check Docker containers

Inside Ubuntu:

```bash
sudo docker ps
```

Expected:

```
nginx-proxy
fastapi-app
postgres-db
```

Example:

```
nginx-proxy
0.0.0.0:80->80/tcp
```

This confirms Nginx is listening on Ubuntu port 80.

---

## Check Nginx logs

```bash
sudo docker compose logs nginx
```

Successful request:

```
"GET /health HTTP/1.1" 200
```

Example:

```
nginx-proxy |
172.18.0.1 - -
"GET /health HTTP/1.1" 200
```

This confirms:

```
Nginx
 |
FastAPI
```

is working.

---

# Solution

Access Ubuntu VM using its IP address.

---

## Step 1: Find Ubuntu VM IP

Inside Ubuntu:

```bash
ip addr
```

Example output:

```
ens33:

inet 192.168.1.120/24
```

The VM address is:

```
192.168.1.120
```

---

## Step 2: Access from Windows Browser

Open:

```
http://192.168.1.120/health
```

Expected response:

```json
{
    "status": "ok"
}
```

---

# Request Flow After Fix

Before:

```
Windows Browser

localhost:80

     |
     v

Windows IIS

     |
     v

404 Not Found
```

---

After:

```
Windows Browser

192.168.1.120:80

     |
     v

Ubuntu VM

     |
     v

Docker Nginx

     |
     v

FastAPI Container

     |
     v

/health API
```

---

# Verification Commands

## Test inside Ubuntu

```bash
curl http://localhost/health
```

Expected:

```json
{
    "status": "ok"
}
```

---

## Test using VM IP

```bash
curl http://192.168.1.120/health
```

Expected:

```json
{
    "status": "ok"
}
```

---

# Alternative Solution

Configure VMware port forwarding.

Example:

```
Windows localhost:8080

        |

        v

Ubuntu VM port 80
```

Then access:

```
http://localhost:8080/health
```

However, using the VM IP is simpler for development.

---

# Lessons Learned

## 1. localhost is machine-specific

`localhost` always means:

```
the current machine
```

It does not mean:

```
all machines in the network
```

---

## 2. Virtual machines create separate network environments

The application was running on:

```
Ubuntu VM
```

but the browser was running on:

```
Windows Host
```

They have different network interfaces.

---

## 3. Production servers work similarly

A real deployment usually looks like:

```
Client

 |
 v

Server IP / Domain

 |
 v

Reverse Proxy

 |
 v

Application Server
```

The VM + Docker setup is similar to a production environment.

---

# Status

Completed:

* [x] FastAPI container running
* [x] PostgreSQL container running
* [x] Nginx reverse proxy working
* [x] Host machine access configured
* [x] External API access verified
