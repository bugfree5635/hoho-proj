<h1 align="center">
  Employee Management API
  <br>
</h1>

<p align="center">
  A production-oriented FastAPI backend demonstrating containerization,
  database management, CI/CD automation, monitoring, and infrastructure operations.
</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.14-blue">
<img src="https://img.shields.io/badge/FastAPI-REST%20API-green">
<img src="https://img.shields.io/badge/PostgreSQL-16-blue">
<img src="https://img.shields.io/badge/Docker-Containerized-blue">
<img src="https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-orange">

</p>

## Overview

Employee Management API is a backend system built with **FastAPI** that simulates a real-world deployment environment.

The project focuses on more than API development. It includes:

- Backend application development
- PostgreSQL database integration
- Docker-based deployment
- Reverse proxy configuration
- Monitoring infrastructure
- CI/CD automation
- Infrastructure troubleshooting


## Architecture

```
                         Client
                           |
                           |
                         Nginx
                           |
                           |
                    FastAPI Application
                           |
                           |
                      PostgreSQL


Monitoring Pipeline:

              Linux Server
                   |
             Node Exporter
                   |
              Prometheus
                   |
               Grafana


CI/CD Pipeline:

              Git Push
                  |
                  |
            GitHub Actions
                  |
                  |
        Install Dependencies
                  |
                  |
        Start PostgreSQL Service
                  |
                  |
              Run pytest
                  |
                  |
                PASS
```

## Features

### Backend Application

- RESTful API with FastAPI
- Employee CRUD operations
- SQLAlchemy ORM integration
- Pydantic validation
- Environment-based configuration
- Health check endpoint
- Automated API testing

### Container Deployment

- Docker containerized application
- Docker Compose orchestration
- PostgreSQL container
- Nginx reverse proxy
- Persistent database storage
- Docker internal networking

### Monitoring

- Linux system monitoring
- CPU metrics
- Memory metrics
- Disk metrics
- Network metrics
- Prometheus metrics collection
- Grafana dashboards

### CI/CD

Implemented GitHub Actions pipeline:

Workflow:

```
Pull Request
      |
      |
GitHub Actions
      |
      |
Install Python dependencies
      |
      |
Start PostgreSQL service container
      |
      |
Run pytest
      |
      |
Merge after successful checks
```

CI validates:

- Application imports
- Database connection
- API tests
- Dependency installation

## Engineering Highlights

During development, several real-world deployment issues were investigated and documented:

### Database

- PostgreSQL hostname resolution failure
- Database environment variable configuration
- Database connection troubleshooting

### Docker

- Container networking problems
- Internal DNS resolution
- Port mapping issues
- Service communication failures

### Monitoring

- Prometheus target configuration
- Grafana datasource problems
- Metrics collection troubleshooting

### Infrastructure

- Ansible SSH configuration
- Server provisioning
- Automated server setup

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
│   ├── prometheus
│   ├── grafana
│   └── node-exporter
│
├── automation
│   ├── backup.sh
│   ├── health_check.sh
│   └── user_create.sh
│
├── ansible
│   ├── setup-server.yml
│   └── docker-install.yml
│
└── docs
    ├── architecture.md
    ├── deployment
    ├── testing
    └── troubleshooting
```

## Technology Stack

| Category | Technology |
|-|-|
| Backend | FastAPI |
| Language | Python 3.14 |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Container | Docker |
| Deployment | Docker Compose |
| Reverse Proxy | Nginx |
| Monitoring | Prometheus + Grafana |
| Metrics | Node Exporter |
| CI/CD | GitHub Actions |
| Automation | Ansible |


## Running Locally

### Clone Repository

```bash
git clone https://github.com/bugfree5635/hoho-proj.git

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

### Start Services


```bash
cd docker

docker compose up -d
```

Check:

```bash
docker ps
```


Expected services:

```
fastapi
postgres
nginx
prometheus
grafana
```

## Access

FastAPI Swagger:

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

CI automatically runs the same tests through GitHub Actions.

## Documentation

Detailed documentation:

```
docs/

├── architecture
├── deployment
├── testing
└── troubleshooting
```

Includes:

- Architecture decisions
- Deployment guides
- Testing strategy
- Production troubleshooting records

## Roadmap

Completed:

- [x] FastAPI backend
- [x] PostgreSQL integration
- [x] Docker deployment
- [x] Nginx reverse proxy
- [x] Prometheus monitoring
- [x] Grafana dashboards
- [x] GitHub Actions CI pipeline
- [x] Ansible automation

Future:

- [ ] Automated production deployment
- [ ] Docker image publishing
- [ ] Kubernetes deployment
- [ ] Database migration automation
- [ ] Security scanning pipeline

# License

MIT License
