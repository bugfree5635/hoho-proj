# Module 03: Monitoring Infrastructure

## Objective

Build monitoring similar to production environments.

## Architecture

    Linux Server
        |
    Node Exporter
        |
    Prometheus
        |
    Grafana

## Monitor

### CPU

-   usage
-   load average

### Memory

-   used memory
-   available memory

### Disk

-   storage usage
-   disk problems

### Network

-   traffic
-   connection status

## Operations Practice

Simulate failures:

-   high CPU
-   stopped service
-   full disk

Then investigate and recover.
