# Prometheus FastAPI Network Resolution Failure

## Problem

After deploying Prometheus monitoring for the FastAPI application, Prometheus target status showed:

```

fastapi DOWN

Error scraping target:

Get "[http://app:8000/metrics](http://app:8000/metrics)":

dial tcp:
lookup app on 127.0.0.11:53:
server misbehaving

```

Prometheus could not collect metrics from the FastAPI container.

---

# Environment

Project architecture:

```
             Grafana
                |
                |
           Prometheus
                |
                |
          FastAPI Metrics
                |
                |
         FastAPI Container
```

```

Docker services:


Application stack:

fastapi-app
postgres-db
nginx-proxy


Monitoring stack:

prometheus
grafana
node-exporter
```

---

# Root Cause

The application and monitoring containers were running on different Docker networks.

Check networks:

```bash
sudo docker network ls
```

Output:

```
NETWORK ID     NAME
xxxx           docker_backend
xxxx           monitoring_default
```

Application containers:

```
docker_backend
```

Monitoring containers:

```
monitoring_default
```

Docker networks are isolated.

The communication path was:

```
Prometheus

     |
     |
     X

FastAPI container
```

Prometheus tried to resolve:

```
app:8000
```

Docker DNS:

```
127.0.0.11
```

could not find the service.

---

# Diagnosis

## Step 1: Check container networks

Check FastAPI:

```bash
sudo docker inspect fastapi-app
```

Example:

```
Networks:

docker_backend
```

Check Prometheus:

```bash
sudo docker inspect prometheus
```

Example:

```
Networks:

monitoring_default
```

The containers were isolated.

---

# Step 2: Check Prometheus configuration

prometheus.yml:

```yaml
scrape_configs:

  - job_name: fastapi

    static_configs:

      - targets:
          - app:8000
```

Prometheus uses Docker DNS:

```
app
 |
 |
Docker DNS
 |
 |
container IP
```

The name `app` only works inside the same Docker network.

---

# Solution

## Step 1: Share the same Docker network

Application compose:

```yaml
networks:

  backend:
```

creates:

```
docker_backend
```

Monitoring compose:

Change from:

```yaml
networks:

  backend:
```

to:

```yaml
networks:

  backend:

    external:

      name: docker_backend
```

---

## Step 2: Restart monitoring stack

Stop containers:

```bash
sudo docker compose down
```

Start again:

```bash
sudo docker compose up -d
```

---

# Verification

## Check networks

```bash
sudo docker network inspect docker_backend
```

Expected:

```
Containers:

fastapi-app
postgres-db
nginx-proxy
prometheus
grafana
node-exporter
```

All services should appear in the same network.

---

## Test DNS from Prometheus

Enter Prometheus container:

```bash
sudo docker exec -it prometheus sh
```

Test:

```bash
wget http://app:8000/metrics
```

Expected:

```
# HELP python_info Python platform information
# TYPE python_info gauge
```

---

# Result

Prometheus target status:

Before:

```
fastapi   DOWN
```

After:

```
fastapi   UP
node      UP
```

Monitoring pipeline:

```
FastAPI

   |
   |
/metrics

   |
   |
Prometheus

   |
   |
Grafana
```

is working.

---

# Lessons Learned

## 1. Docker DNS only works inside the same network

Example:

Works:

```
container A
 |
same Docker network
 |
container B
```

Does not work:

```
container A
 |
network A

container B
 |
network B
```

---

## 2. Docker Compose projects create separate networks

Running:

```bash
docker compose up
```

in different directories creates independent networks.

Example:

Application:

```
docker_backend
```

Monitoring:

```
monitoring_default
```

They cannot communicate automatically.

---

## 3. Production systems use service discovery

The same concept exists in:

Docker:

```
app:8000
```

Kubernetes:

```
fastapi-service.default.svc.cluster.local
```

Cloud:

```
Load Balancer DNS
```

Service discovery is required for distributed systems.

---

# Status

Completed:

* [x] Prometheus deployed
* [x] Grafana deployed
* [x] Node Exporter deployed
* [x] Docker network problem identified
* [x] Monitoring and application networks combined
* [x] FastAPI metrics reachable
* [x] Prometheus scraping successful
