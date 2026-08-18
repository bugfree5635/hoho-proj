# Alembic Missing Revision

## Problem

When running an Alembic command such as:

```bash
alembic revision --autogenerate -m "initial migration"
```

Alembic returns:

```text
ERROR [alembic.util.messaging] Can't locate revision identified by '549ba30a27f0'
FAILED: Can't locate revision identified by '549ba30a27f0'
```

## Cause

The PostgreSQL database references an Alembic revision that does not exist in the local project's migration files.

For example, the database may contain:

```text
alembic_version
----------------
549ba30a27f0
```

but the local project contains:

```text
alembic/versions/

4838c302a2a5_initial_migration.py
7dda80726bae_add_users_table.py
```

There is no migration file for:

```text
549ba30a27f0
```

This can happen when:

* a migration file was deleted
* migration files were not committed to Git
* the project was copied from another environment
* the database was created using a different migration history
* migration branches were changed or recreated

## Debug

Check the current database revision:

```bash
alembic current
```

Check the local migration history:

```bash
alembic history
```

Check the migration heads:

```bash
alembic heads
```

Check the migration files:

```bash
ls alembic/versions/
```

You can also check the database directly:

```sql
SELECT * FROM alembic_version;
```

Compare the revision stored in PostgreSQL with the revision IDs in:

```text
alembic/versions/
```

## Solution

### Option 1: Restore the missing migration

If the missing migration exists in Git or another environment, restore it:

```bash
git log -- alembic/versions/
```

Then restore the missing migration file.

After restoring it:

```bash
alembic history
alembic current
```

Then retry the Alembic command.

### Option 2: Reset the development database

If this is only a local development database and the data is not important, you can recreate the database.

For example, with Docker Compose:

```bash
sudo docker compose down -v
sudo docker compose up -d
```

Then run:

```bash
alembic upgrade head
```

This creates a fresh database using the migration history currently stored in the project.

**Do not use this approach for a production database unless you intentionally want to destroy its data.**

### Option 3: Fix the migration state manually

If the database schema is already correct but the Alembic revision state is wrong, the migration state may need to be repaired with:

```bash
alembic stamp <revision>
```

For example:

```bash
alembic stamp head
```

`stamp` changes Alembic's recorded revision without running the migration.

Use this carefully. The database schema must actually match the revision you stamp it with.

## Verify

Check the migration history:

```bash
alembic history
```

Then:

```bash
alembic current
```

Finally:

```bash
alembic upgrade head
```

If the database is synchronized with the migration files, Alembic should no longer report the missing revision.

## Lesson

Alembic stores migration state inside the database:

```text
PostgreSQL
    |
    v
alembic_version
    |
    v
549ba30a27f0
```

while the actual migration code lives in the project:

```text
alembic/versions/
```

These two must correspond.

The key lesson is:

> **Never delete, rename, or recreate an Alembic migration casually after it has already been applied to a database.**

Migration files are part of the database's history, not just temporary files used to create tables.
