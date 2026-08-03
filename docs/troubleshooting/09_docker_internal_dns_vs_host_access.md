# Docker Internal DNS vs Host Access

## Problem

Cannot open:

```
http://prometheus:9093
```

Browser error:

```
ERR_NAME_NOT_RESOLVED
```

---

# Environment

Monitoring architecture:

```
Grafana

   |

Prometheus

   |

Node Exporter
```

Docker Compose services:

```yaml
services:

  prometheus:

    container_name: prometheus
```

---

# Investigation

## Docker service name

Inside Docker network:

```
prometheus
```

is a DNS name.

Example:

Grafana container:

```
http://prometheus:9090
```

works.

Because:

```
grafana container
        |
        |
 docker network DNS
        |
        |
 prometheus container
```

---

## Browser request

Browser runs on:

```
Host machine
```

not inside Docker.

Therefore:

```
localhost
```

is the host.

The host does not know:

```
prometheus
```

as a DNS name.

---

# Root Cause

There are two different networks.

## Docker network

Used by containers:

```
grafana

   |

prometheus
```

DNS:

```
prometheus
```

works.

---

## Host network

Used by browser:

```
Laptop

 |

localhost:9093
```

Docker publishes ports here.

---

# Solution

## For Grafana datasource

Use:

```
http://prometheus:9090
```

because Grafana runs inside Docker.

---

## For browser

Use:

```
http://localhost:9093
```

because browser runs outside Docker.

---

# Verify

Enter Grafana container:

```bash
docker exec -it grafana bash
```

Test:

```bash
curl http://prometheus:9090
```

Expected:

Prometheus HTML response.

---

# Lessons Learned

Always ask:

"Where is this command running?"

Possible locations:

```
Host machine

Docker container

Docker network

Cloud server
```

The same hostname may work in one environment but fail in another.

