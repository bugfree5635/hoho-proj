# Database Backup and Restore

## Overview

The application uses PostgreSQL to store persistent data.

Database backup and restore provides a way to protect application data and recover it after accidental deletion, database failure, or other data-loss events.

```text
FastAPI
   |
   v
PostgreSQL
   |
   +── users
   +── employees
   |
   v
Database Backup
   |
   v
backup.dump
```

## Backup

PostgreSQL provides `pg_dump` for creating database backups.

Example:

```bash
docker compose exec -T postgres \
    pg_dump \
    -U admin \
    -Fc \
    company > backup.dump
```

The `-Fc` option creates a PostgreSQL custom-format backup.

The recommended backup location is:

```text
backups/
```

Backup files should not be committed to Git.

Add the following to `.gitignore`:

```gitignore
backups/
```

## Automated Backup

The project provides:

```text
automation/
└── backup_db.sh
```

Run:

```bash
./automation/backup_db.sh
```

The script creates a timestamped backup:

```text
backups/
└── company_20260819_195000.dump
```

The timestamp allows multiple backups to be kept without overwriting previous backups.

## Restore

PostgreSQL custom-format backups can be restored with `pg_restore`.

Example:

```bash
docker compose exec -T postgres \
    pg_restore \
    -U admin \
    -d company \
    --clean \
    --if-exists \
    < backup.dump
```

The project provides:

```text
automation/
├── backup_db.sh
└── restore_db.sh
```

Run:

```bash
./automation/restore_db.sh backups/company_20260819_195000.dump
```

## Verify Backup

After restoring, verify that the database tables exist:

```bash
docker compose exec postgres \
    psql -U admin -d company \
    -c "\dt"
```

Verify application data:

```bash
docker compose exec postgres \
    psql -U admin -d company \
    -c "SELECT * FROM employees;"
```

Verify users:

```bash
docker compose exec postgres \
    psql -U admin -d company \
    -c "SELECT id, username FROM users;"
```

## Recovery Test

Backups should be tested through an actual restore operation.

The development recovery test is:

```text
Create test data
      |
      v
Create backup
      |
      v
Simulate data loss
      |
      v
Restore backup
      |
      v
Verify data
```

Example:

```sql
INSERT INTO employees (name, email, department)
VALUES
    ('Henry', 'henry@example.com', 'Engineering'),
    ('Alice', 'alice@example.com', 'Security'),
    ('Bob', 'bob@example.com', 'DevOps');
```

Create the backup:

```bash
./automation/backup_db.sh
```

Simulate data loss:

```sql
DELETE FROM employees;
```

Restore:

```bash
./automation/restore_db.sh backups/company_YYYYMMDD_HHMMSS.dump
```

Verify:

```sql
SELECT * FROM employees;
```

The original records should be restored.

## Backup and Deployment

Database backup should be considered as part of the deployment process.

A production deployment can follow this sequence:

```text
New application version
        |
        v
Run tests
        |
        v
Build Docker image
        |
        v
Backup database
        |
        v
Deploy new version
        |
        v
Health check
        |
    +---+---+
    |       |
 success   failure
    |       |
    v       v
  Keep   Rollback
          |
          v
    Previous image
```

## Important Distinction

Application rollback and database recovery solve different problems.

### Application rollback

```text
Broken Docker image
       |
       v
Previous Docker image
```

### Database migration rollback

```text
Alembic migration 003
       |
       v
Alembic migration 002
```

### Database recovery

```text
Lost database data
       |
       v
Backup
       |
       v
Restore
```

A Docker image rollback does not restore deleted database data.

## Security

Database backups may contain sensitive information.

Therefore:

* Do not commit backups to Git.
* Do not expose backups through the web server.
* Restrict access to backup files.
* Use encrypted storage for production backups.
* Keep backups outside the application container.
* Test restoration regularly.

## Production Considerations

For a production deployment, backups should eventually be stored outside the application server.

Example:

```text
Production PostgreSQL
        |
        v
Backup job
        |
        v
Object Storage
        |
        +── backup-2026-08-19.dump
        +── backup-2026-08-18.dump
        +── backup-2026-08-17.dump
```

Possible future improvements:

* Scheduled backups
* Backup retention
* Encrypted backups
* Remote/object storage
* Automated restore testing
* Monitoring backup success/failure
* Recovery Point Objective (RPO)
* Recovery Time Objective (RTO)
