# Database Architecture

## Overview

This project uses PostgreSQL as the primary application database.

The database is responsible for:

- storing application data
- maintaining data consistency
- enforcing relationships between entities
- supporting application operations
- providing persistent storage

Architecture:

```

```
            User

             |

             v

          Nginx

             |

             v

      FastAPI Application

             |

             |

      SQLAlchemy ORM

             |

             |

      PostgreSQL Database

             |

             |

      Docker Volume Storage
```

```

---

# Database Components

## Application Layer

The FastAPI application communicates with PostgreSQL through SQLAlchemy.

Flow:

```

API Request

 |

 v

FastAPI Endpoint

 |

 v

SQLAlchemy Session

 |

 v

PostgreSQL Query

 |

 v

Database Response
```

Example:

```python
db.query(Employee).all()
```

SQLAlchemy converts Python operations into SQL queries.

---

# PostgreSQL Database

## Production Database

Example configuration:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

The application connects using:

```
postgres:5432
```

inside the Docker network.

---

# Docker Network Architecture

Production environment:

```
Docker Network: backend


+----------------+

| FastAPI        |

| container      |

+----------------+

        |

        |

        v


+----------------+

| PostgreSQL     |

| container      |

+----------------+
```

Containers communicate using service names.

Example:

```env
DATABASE_HOST=postgres
```

not:

```env
DATABASE_HOST=localhost
```

Reason:

Inside containers:

```
localhost
    |
    |
    v
current container
```

Therefore:

FastAPI container:

```
localhost:5432

      X

PostgreSQL container
```

Correct:

```
postgres:5432

      |

      v

PostgreSQL container
```

---

# Database Storage

PostgreSQL stores data inside:

```
/var/lib/postgresql/data
```

Docker maps this directory:

```yaml
volumes:

  - postgres_data:/var/lib/postgresql/data
```

Architecture:

```
PostgreSQL Container


        |

        |


Docker Volume


        |

        |


Host Machine Disk
```

The database survives container recreation.

Example:

Remove container:

```bash
docker rm postgres-db
```

Data remains:

```
postgres_data
```

---

# Database Schema Management

The project currently creates tables using:

```python
Base.metadata.create_all(bind=engine)
```

Example:

```
Application Startup

        |

        v

SQLAlchemy Metadata

        |

        v

Create Tables
```

This is suitable for:

* learning projects
* prototypes
* development

---

# Production Migration Strategy

Production systems use Alembic migrations.

Architecture:

```
Developer

   |

   |

Create migration

   |

   |

Alembic

   |

   |

PostgreSQL Database
```

Example:

Create migration:

```bash
alembic revision --autogenerate -m "add employee table"
```

Apply:

```bash
alembic upgrade head
```

Benefits:

* version controlled schema changes
* safe database upgrades
* rollback support

---

# Database Environments

The project separates databases.

## Development

```
company_dev
```

Purpose:

* local development
* testing new features

## Testing

```
company_test
```

Purpose:

* automated tests
* CI pipeline

## Production

```
company
```

Purpose:

* real application data

Architecture:

```
                Application


        |          |          |


        v          v          v


   company_dev company_test company

```

Production data is never used by tests.

---

# Database Backup Strategy

Production databases require backups.

Example:

```
PostgreSQL

     |

     |

pg_dump

     |

     |

backup.sql

     |

     |

Remote Storage
```

Backup command:

```bash
pg_dump company > backup.sql
```

Restore:

```bash
psql company < backup.sql
```

---

# Database Monitoring

Important metrics:

## Storage

Monitor:

* database size
* table growth
* disk usage

Example:

```sql
SELECT pg_size_pretty(
pg_database_size('company')
);
```

---

## Connections

Monitor:

```sql
SELECT count(*)
FROM pg_stat_activity;
```

Important because too many connections can reduce performance.

---

## Query Performance

Monitor:

* slow queries
* missing indexes
* high CPU queries

Common tools:

* PostgreSQL logs
* Prometheus
* Grafana
* Datadog

---

# Security Considerations

## Password Management

Do not store passwords in code.

Bad:

```python
DATABASE_PASSWORD="password"
```

Good:

```env
DATABASE_PASSWORD=password
```

Production:

Use:

* GitHub Secrets
* AWS Secrets Manager
* Hashicorp Vault

---

## Database Access Control

Use least privilege.

Example:

Application user:

```
company_app_user
```

Permissions:

```
SELECT
INSERT
UPDATE
DELETE
```

Avoid using:

```
postgres superuser
```

for applications.

---

# High Availability Future Architecture

Current:

```
FastAPI

   |

PostgreSQL
```

Future production:

```
              FastAPI

                  |

                  |

          PostgreSQL Primary

                  |

                  |

          Streaming Replication

                  |

                  |

          PostgreSQL Replica
```

Benefits:

* failover
* read scaling
* higher availability

---

# Summary

Current database architecture:

```
FastAPI
   |
SQLAlchemy
   |
PostgreSQL
   |
Docker Volume
```

The project provides:

* isolated database environments
* persistent storage
* container networking
* automated testing database
* production-style database management

Future improvements:

* Alembic migrations
* automated backups
* database monitoring
* high availability
* managed PostgreSQL service
