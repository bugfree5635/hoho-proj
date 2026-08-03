# Prometheus Container Port Mapping Failure

## Problem

Prometheus container failed to start.

Error:

```
failed to bind host port 0.0.0.0:9090/tcp:
address already in use
```

or browser cannot open Prometheus.

---

# Environment

Project:

```
monitoring/

├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml
└── grafana/
```

Docker Compose:

```yaml
prometheus:

  image: prom/prometheus

  ports:

    - "9093:9093"
```

---

# Investigation

## Step 1: Check running containers

Command:

```bash
docker ps
```

Example:

```
CONTAINER ID   IMAGE
xxxx           prometheus
yyyy           node-exporter
```

---

## Step 2: Check used ports

Command:

```bash
sudo ss -tulpn
```

Example:

```
LISTEN 0 4096 0.0.0.0:9090
```

Port 9090 is already occupied.

---

# Root Cause

Docker port mapping format:

```
HOST_PORT:CONTAINER_PORT
```

Prometheus inside container listens on:

```
9090
```

not:

```
9093
```

Wrong:

```yaml
ports:

 - "9093:9093"
```

Docker tries to map:

```
localhost:9093
        |
        |
container:9093
```

but Prometheus does not listen there.

---

# Solution

Correct configuration:

```yaml
prometheus:

  image: prom/prometheus

  ports:

    - "9093:9090"
```

Meaning:

Host:

```
http://localhost:9093
```

connects to:

```
Prometheus container port 9090
```

---

# Verify

Restart:

```bash
docker compose down

docker compose up -d
```

Check:

```bash
docker ps
```

Expected:

```
0.0.0.0:9093->9090/tcp
```

Open:

```
http://localhost:9093
```

---

# Lessons Learned

Docker networking requires understanding:

```
HOST PORT
    |
    |
CONTAINER PORT
```

The external port can be different from the internal application port.
