# GitHub Actions Promtool Entrypoint Failure

## Problem

GitHub Actions failed when validating the Prometheus configuration.

The CI command was:

```bash
docker run --rm \
  -v /home/runner/work/hoho-proj/hoho-proj/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus \
  promtool check config /etc/prometheus/prometheus.yml
```

The error was:

```text
Error parsing command line arguments: unexpected promtool

prometheus: error: unexpected promtool
```

The CI job exited with:

```text
Process completed with exit code 1
```

---

## Cause

The problem was caused by the Docker image entrypoint.

The `prom/prometheus` image is designed to start the Prometheus server by default.

Conceptually, the image has an entrypoint similar to:

```text
prometheus
```

The original Docker command:

```bash
docker run prom/prometheus promtool check config /etc/prometheus/prometheus.yml
```

was effectively executed as:

```bash
prometheus promtool check config /etc/prometheus/prometheus.yml
```

The `prometheus` server binary received `promtool` as an unexpected command-line argument.

Therefore Prometheus returned:

```text
Error parsing command line arguments: unexpected promtool
```

---

## Debug

The GitHub Actions log showed:

```text
Error parsing command line arguments: unexpected promtool

prometheus: error: unexpected promtool
```

This indicated that the `promtool` command was being passed to the wrong executable.

The expected command was:

```bash
promtool check config /etc/prometheus/prometheus.yml
```

However, Docker was using the default image entrypoint:

```text
prometheus
```

The command was therefore effectively:

```text
prometheus promtool check config
```

instead of:

```text
promtool check config
```

---

## Solution

Override the Docker image entrypoint using `--entrypoint`.

The corrected GitHub Actions step is:

```yaml
- name: Validate Prometheus configuration
  run: |
    docker run --rm \
      --entrypoint promtool \
      -v ${{ github.workspace }}/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
      prom/prometheus \
      check config /etc/prometheus/prometheus.yml
```

The `--entrypoint` option replaces the default:

```text
prometheus
```

with:

```text
promtool
```

Docker then executes:

```text
promtool check config /etc/prometheus/prometheus.yml
```

---

## Verify

Push the updated workflow and run the GitHub Actions pipeline again.

A successful validation should produce output similar to:

```text
Checking /etc/prometheus/prometheus.yml
SUCCESS: /etc/prometheus/prometheus.yml is valid
```

The CI job should complete successfully.

---

## Lesson

Docker images may define an `ENTRYPOINT`.

When additional arguments are provided to:

```bash
docker run image command
```

they may be appended to the existing entrypoint.

Conceptually:

```text
Docker image

ENTRYPOINT:
prometheus
```

Running:

```bash
docker run prom/prometheus promtool check config
```

can result in:

```text
prometheus promtool check config
```

If a different executable inside the image needs to be executed, override the entrypoint:

```bash
docker run \
  --entrypoint promtool \
  prom/prometheus \
  check config
```

Understanding Docker `ENTRYPOINT` and `CMD` behavior is important when using containers as CI tools.
