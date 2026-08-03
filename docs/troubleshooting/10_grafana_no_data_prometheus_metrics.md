# Grafana No Data From Prometheus Metrics

## Problem

Grafana dashboard shows:

```
No Data
```

CPU, memory, disk metrics are empty.

---

# Architecture

Monitoring stack:

```
Linux Server

     |

Node Exporter

     |

Prometheus

     |

Grafana
```

---

# Investigation

## Step 1: Check containers

Command:

```bash
docker ps
```

Expected:

```
node-exporter
prometheus
grafana
```

---

## Step 2: Check Prometheus targets

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

UP
```

---

# Possible Causes

## Cause 1: Prometheus cannot reach Node Exporter

Check:

```bash
docker logs prometheus
```

Example error:

```
connection refused
```

---

## Cause 2: Wrong prometheus.yml

Example:

Wrong:

```yaml
targets:

 - localhost:9100
```

Why?

Inside Prometheus container:

```
localhost
```

means Prometheus itself.

---

Correct:

```yaml
scrape_configs:

- job_name: node-exporter

  static_configs:

  - targets:

    - node-exporter:9100
```

Because:

```
prometheus container

        |

docker DNS

        |

node-exporter container
```

---

## Cause 3: Grafana datasource incorrect

Grafana runs inside Docker.

Wrong:

```
http://localhost:9093
```

Inside container:

```
localhost
```

means Grafana container.

---

Correct:

```
http://prometheus:9090
```

---

# Verification

## Check Prometheus metrics

Open:

```
http://localhost:9093/targets
```

Target:

```
node-exporter

State: UP
```

---

## Check Node Exporter

Open:

```
http://localhost:9100/metrics
```

Expected:

```
node_cpu_seconds_total

node_memory_MemAvailable_bytes
```

---

## Check Grafana

Datasource:

```
Connections

 |

Data sources

 |

Prometheus
```

URL:

```
http://prometheus:9090
```

Click:

```
Save & Test
```

Expected:

```
Data source is working
```

---

# Lessons Learned

Monitoring debugging order:

```
1. Node Exporter

      |

2. Prometheus scrape target

      |

3. Grafana datasource

      |

4. Dashboard query
```

Never debug Grafana first.

The data pipeline must work from the bottom upward.

These three fit your current project because they record the exact problems you hit while building:

* Prometheus port `9090` vs host `9093`
* Docker DNS (`prometheus`) vs browser (`localhost`)
* Grafana → Prometheus → Node Exporter data flow

This is the style a DevOps/SRE team would keep as an internal incident record.
