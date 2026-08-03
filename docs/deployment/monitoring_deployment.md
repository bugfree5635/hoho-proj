# Monitoring Infrastructure Deployment

## Objective

Deploy production-style monitoring infrastructure using:

- Node Exporter
- Prometheus
- Grafana

The monitoring system collects Linux server metrics and provides visualization dashboards.

---

# Architecture

```
                    Browser
                       |
                       |
                       v

                 Grafana :3000

                       |
                       |
                       v

              Prometheus :9090

                       |
                       |
                       v

          Node Exporter :9100

                       |
                       |
                       v

                 Linux Host
```

---

# Components

## Node Exporter

Purpose:

Collect Linux system metrics.

Metrics include:

- CPU usage
- Memory usage
- Disk usage
- Network traffic
- System load


Container:

```
prom/node-exporter
```

Port:

```
9100
```

---

## Prometheus

Purpose:

Collect and store metrics from exporters.

Responsibilities:

- scrape metrics
- store time-series data
- provide query interface


Container:

```
prom/prometheus
```

Internal port:

```
9090
```

Host access:

```
localhost:9093
```

---

## Grafana

Purpose:

Visualize monitoring data.

Responsibilities:

- create dashboards
- display CPU/memory/disk graphs
- connect to Prometheus datasource


Container:

```
grafana/grafana
```

Port:

```
3000
```

---

# Directory Structure

```
monitoring/

├── docker-compose.yml

├── prometheus/

│   ├── prometheus.yml

│   └── alerts.yml

└── grafana/

    └── dashboards/
```

---

# Step 1: Configure Prometheus

File:

```
monitoring/prometheus/prometheus.yml
```

Example:

```yaml
global:

  scrape_interval: 15s


scrape_configs:

  - job_name: node-exporter

    static_configs:

      - targets:

          - node-exporter:9100
```

Important:

Prometheus runs inside Docker.

Therefore:

Correct:

```
node-exporter:9100
```

Incorrect:

```
localhost:9100
```

Docker provides internal DNS service discovery.

---

# Step 2: Docker Compose Configuration

File:

```
monitoring/docker-compose.yml
```

Example:

```yaml
services:


  node-exporter:

    image: prom/node-exporter

    container_name: node-exporter

    ports:

      - "9100:9100"

    restart: always



  prometheus:

    image: prom/prometheus

    container_name: prometheus

    volumes:

      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

    ports:

      - "9093:9090"

    depends_on:

      - node-exporter

    restart: always



  grafana:

    image: grafana/grafana

    container_name: grafana

    ports:

      - "3000:3000"

    depends_on:

      - prometheus

    restart: always
```

---

# Step 3: Start Monitoring Stack

Go to monitoring directory:

```bash
cd monitoring
```

Start containers:

```bash
sudo docker compose up -d
```

Check status:

```bash
sudo docker ps
```

Expected:

```
node-exporter
prometheus
grafana
```

---

# Step 4: Verify Node Exporter

Open:

```
http://localhost:9100/metrics
```

Expected:

Large metric output:

```
node_cpu_seconds_total

node_memory_MemTotal_bytes

node_filesystem_size_bytes
```

---

# Step 5: Verify Prometheus

Open:

```
http://localhost:9093
```

Go to:

```
Status
 |
 Targets
```

Expected:

```
node-exporter:9100

State:

UP
```

---

# Step 6: Configure Grafana

Open:

```
http://localhost:3000
```

Default login:

```
username:
admin

password:
admin
```

Create Prometheus datasource:

```
Connections

    |

Data Sources

    |

Prometheus
```

URL:

```
http://prometheus:9090
```

Important:

Use Docker service name.

Do not use:

```
http://localhost:9093
```

because Grafana is running inside Docker.

---

# Step 7: Create Monitoring Dashboard

Recommended panels:

## CPU Usage

PromQL:

```promql
100 -
(avg by(instance)
(rate(node_cpu_seconds_total{
mode="idle"
}[5m])) * 100)
```

---

## Memory Usage

PromQL:

```promql
(
1 -
node_memory_MemAvailable_bytes
/
node_memory_MemTotal_bytes
)
*100
```

---

## Disk Usage

PromQL:

```promql
(
node_filesystem_size_bytes
-
node_filesystem_avail_bytes
)
/
node_filesystem_size_bytes
*100
```

---

# Troubleshooting

## Problem: Grafana shows No Data

Check:

```bash
sudo docker ps
```

Verify:

```
node-exporter running
prometheus running
grafana running
```

---

Check Prometheus targets:

```
http://localhost:9093

Status

Targets
```

Target should be:

```
node-exporter:9100 UP
```

---

## Problem: Prometheus cannot scrape Node Exporter

Cause:

Wrong hostname.

Incorrect:

```yaml
targets:

  - localhost:9100
```

Correct:

```yaml
targets:

  - node-exporter:9100
```

---

## Problem: Cannot access Prometheus

Check port mapping:

```yaml
ports:

  - "9093:9090"
```

Explanation:

```
HOST_PORT:CONTAINER_PORT
```

Prometheus listens internally on:

```
9090
```

---

# Verification Checklist

Before considering monitoring deployment complete:

- [x] Node Exporter running
- [x] Prometheus container running
- [x] Prometheus target shows UP
- [x] Grafana accessible
- [x] Grafana connected to Prometheus
- [x] CPU dashboard working
- [x] Memory dashboard working
- [x] Disk dashboard working

---

# Key Lessons Learned

1. Monitoring systems are usually separated into:

```
Collection

    |

Storage

    |

Visualization
```

2. Docker service discovery allows containers to communicate:

```
grafana

   |

prometheus:9090
```

3. Host access and container access are different:

Browser:

```
localhost:3000
localhost:9093
```

Docker:

```
prometheus:9090
node-exporter:9100
```

4. Always verify monitoring from bottom to top:

```
Node Exporter

    |

Prometheus

    |

Grafana
```
````

This fits your current portfolio architecture because now your project shows:

```
Nginx
 |
FastAPI
 |
PostgreSQL

+
 
Node Exporter
 |
Prometheus
 |
Grafana
```

This is much closer to a real small production environment.
