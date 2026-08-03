# Prometheus Container Port Mapping Failure

## Problem

When deploying the monitoring infrastructure:

```bash
sudo docker compose up -d
```

Prometheus container failed to start.

Initial error:

```
failed to bind host port 0.0.0.0:9090/tcp:
address already in use
```

After changing the port:

```yaml
ports:
  - "9093:9093"
```

The container started, but accessing:

```
http://localhost:9093
```

returned:

```
ERR_EMPTY_RESPONSE
```

Prometheus web interface was unavailable.

---

# Environment

Monitoring architecture:

```
Linux Server

    |
    |
Node Exporter
    |
    |
Prometheus
    |
    |
Grafana (future)
```

Docker Compose:

```yaml
services:

  node-exporter:

    image: prom/node-exporter

    container_name: node-exporter

    ports:
      - "9100:9100"


  prometheus:

    image: prom/prometheus

    container_name: prometheus

    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

    ports:
      - "9093:9093"

    depends_on:

      - node-exporter
```

---

# Investigation

## Step 1: Check running containers

Command:

```bash
sudo docker ps
```

Found another service was already using:

```
9090
```

Prometheus default web port.

Prometheus listens inside the container on:

```
9090
```

---

## Step 2: Understand Docker Port Mapping

Docker port format:

```
HOST_PORT:CONTAINER_PORT
```

Example:

```
9093:9090
```

means:

```
Linux Host

localhost:9093

        |
        |
        v

Docker Container

Prometheus:9090
```

The host port can be different.

The container port must match the application listening port.

---

# Root Cause

The wrong port mapping was configured:

```yaml
ports:

  - "9093:9093"
```

This created:

```
Host

localhost:9093

        |
        |
        v

Container

Prometheus:9093
```

However Prometheus does not listen on port:

```
9093
```

Prometheus default port:

```
9090
```

Therefore Docker forwarded traffic to a port where no service was running.

---

# Solution

Change Docker Compose configuration.

Before:

```yaml
ports:

  - "9093:9093"
```

After:

```yaml
ports:

  - "9093:9090"
```

Now the traffic flow becomes:

```
Browser

localhost:9093

        |
        |
        v

Docker Host Port

9093

        |
        |
        v

Prometheus Container

9090
```

---

# Restart Container

Stop old containers:

```bash
sudo docker compose down
```

Start again:

```bash
sudo docker compose up -d
```

---

# Verification

Check container status:

```bash
sudo docker ps
```

Expected:

```
prom/prometheus

0.0.0.0:9093->9090/tcp
```

Check Prometheus logs:

```bash
sudo docker logs prometheus
```

Healthy output:

```
Server is ready to receive web requests.
```

Open browser:

```
http://localhost:9093
```

Prometheus dashboard should load.

---

# Additional Issue: Port Already In Use

If the original error appears:

```
failed to bind host port 0.0.0.0:9090/tcp:
address already in use
```

Find the process using the port:

```bash
sudo lsof -i :9090
```

or:

```bash
sudo docker ps
```

Possible solutions:

### Option 1: Stop the existing service

```bash
sudo docker stop <container_name>
```

### Option 2: Use another host port

Example:

```yaml
ports:

  - "9093:9090"
```

---

# Key Lessons Learned

1. Docker port mapping format is:

```
HOST_PORT:CONTAINER_PORT
```

2. The host port can be customized.

Example:

```
9093:9090
```

means:

```
User accesses 9093
Prometheus runs on 9090
```

3. Always check application default ports.

Common examples:

| Service | Container Port |
|---|---|
| FastAPI | 8000 |
| Nginx | 80 |
| PostgreSQL | 5432 |
| Prometheus | 9090 |
| Node Exporter | 9100 |

4. A container running does not mean the service is reachable.

Always verify:

- container status
- port mapping
- application listening port
- service logs

5. Container networking problems are usually caused by:

- wrong port mapping
- port conflicts
- wrong container network
- application not listening
- incorrect configuration

```
Symptom
  |
  v
Browser cannot access service
  |
  v
Check docker status
  |
  v
Check port mapping
  |
  v
Understand container internal port
  |
  v
Fix configuration
  |
  v
Verify logs and service availability
```

It is exactly the type of small production issue a junior DevOps/sysadmin engineer would handle.
