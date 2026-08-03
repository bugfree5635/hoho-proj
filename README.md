<h1 align="center">
  Employee Management API
  <br>
</h1>

<h4 align="center">
A production-style FastAPI application with Docker deployment, PostgreSQL, Nginx, and monitoring infrastructure.
</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-green?style=flat-square" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square" alt="Docker">
  <img src="https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-orange?style=flat-square" alt="Monitoring">
</p>

## Overview

Employee Management API is a backend application built with FastAPI and designed to simulate a real-world production deployment environment.

The project focuses not only on application development, but also on:

* Container deployment
* Database management
* Reverse proxy configuration
* Infrastructure monitoring
* Troubleshooting and operations practice

## Architecture

```
                    Client

                      |

                    Nginx

                      |

              FastAPI Container

                      |

              PostgreSQL Database


Monitoring:

        Linux Server

              |

        Node Exporter

              |

          Prometheus

              |

           Grafana
```

## Features

### Application

* RESTful API built with FastAPI
* Employee CRUD operations
* Pydantic schema validation
* SQLAlchemy database integration
* Environment-based configuration management
* Health check endpoint

### Deployment

* Docker containerized application
* Docker Compose infrastructure
* PostgreSQL database container
* Nginx reverse proxy
* Persistent database volumes
* Internal Docker networking

### Monitoring

* Linux system monitoring
* CPU usage monitoring
* Memory monitoring
* Disk monitoring
* Network monitoring
* Prometheus metrics collection
* Grafana dashboards

### Operations Practice

The project includes troubleshooting records for common production issues:

* PostgreSQL hostname resolution failure
* Environment variable loading problems
* Python dependency compatibility issues
* Docker installation issues
* Container port mapping problems
* Docker internal DNS problems
* Grafana monitoring data issues

## Project Structure

```
.
├── app
│   ├── api
│   ├── config
│   ├── database
│   ├── schemas
│   ├── tests
│   ├── Dockerfile
│   └── main.py
│
├── docker
│   └── docker-compose.yml
│
├── nginx
│   └── nginx.conf
│
├── monitoring
│   ├── prometheus.yml
│   ├── alerts.yml
│   └── grafana
│
├── automation
│   ├── backup.sh
│   ├── health_check.sh
│   └── user_create.sh
│
└── docs
    ├── architecture.md
    ├── deployment
    ├── testing
    └── troubleshooting
```

## Technology Stack

| Component      | Technology           |
| -------------- | -------------------- |
| Backend        | FastAPI              |
| Language       | Python               |
| Database       | PostgreSQL           |
| ORM            | SQLAlchemy           |
| Container      | Docker               |
| Deployment     | Docker Compose       |
| Reverse Proxy  | Nginx                |
| Monitoring     | Prometheus + Grafana |
| System Metrics | Node Exporter        |

## Installation

### Clone Repository

```bash
git clone <repository-url>

cd hoho-proj
```

### Configure Environment Variables

Create:

```
app/.env
```

Example:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

### Start Application

```bash
cd docker

docker compose up -d
```

Check containers:

```bash
docker ps
```

Expected:

```
fastapi-app
postgres-db
nginx-proxy
```

## Access

FastAPI:

```
http://localhost/docs
```

Health Check:

```
http://localhost/health
```

Prometheus:

```
http://localhost:9093
```

Grafana:

```
http://localhost:3000
```

## Testing

Run tests:

```bash
pytest
```

Example:

```
1 passed
```

## Documentation

Detailed documentation:

* Architecture design
* Deployment process
* Testing strategy
* Monitoring setup
* Troubleshooting records

Location:

```
docs/
```

## Development Roadmap

Completed:

* [x] FastAPI backend
* [x] PostgreSQL integration
* [x] Docker deployment
* [x] Nginx reverse proxy
* [x] Prometheus monitoring
* [x] Grafana dashboards

Future:

* [ ] CI/CD pipeline
* [ ] GitHub Actions
* [ ] Automated deployment
* [ ] Ansible server provisioning
* [ ] Kubernetes deployment

## License

This project is released under the MIT License.
