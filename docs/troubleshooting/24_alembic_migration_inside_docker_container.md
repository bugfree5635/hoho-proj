# Alembic Migration Inside Docker Container

## Problem

When working with a Dockerized FastAPI application, Alembic commands are executed inside the application container:

```bash
sudo docker exec -it fastapi-app bash
```

Then:

```bash
alembic revision --autogenerate -m "add users table"
```

or:

```bash
alembic upgrade head
```

The migration appears to work inside the container, but the migration file may not appear on the host machine.

For example, inside the container:

```text
/app/alembic/versions/
├── 4838c302a2a5_initial_migration.py
└── 7dda80726bae_add_users_table.py
```

but on the host:

```text
hoho-proj/alembic/versions/
└── 4838c302a2a5_initial_migration.py
```

## Cause

A Docker container has its own filesystem.

The path:

```text
/app/alembic/versions/
```

inside the container is not automatically the same filesystem as:

```text
~/practice/hoho-proj/alembic/versions/
```

on the host.

There are two important cases.

### Case 1: Directory is mounted as a volume

For example:

```yaml
services:
  fastapi:
    volumes:
      - .:/app
```

Then:

```text
Host
~/practice/hoho-proj
        │
        │ bind mount
        ↓
Container
/app
```

Changes made inside `/app` are visible on the host.

### Case 2: Directory is not mounted

If the Docker image contains the application:

```dockerfile
COPY . /app
```

but there is no bind mount:

```text
Host
~/practice/hoho-proj
        │
        │ image build
        ↓
Docker image
        │
        ↓
Container
/app
```

The container has its own copy of the files.

A migration created inside the container will remain inside that container.

## Debug

Check whether the project directory is mounted:

```bash
sudo docker inspect fastapi-app
```

Look for:

```text
Mounts
```

You can also use:

```bash
sudo docker inspect fastapi-app \
  --format '{{json .Mounts}}'
```

Check the migration files inside the container:

```bash
sudo docker exec -it fastapi-app ls -la /app/alembic/versions/
```

Then check the host:

```bash
ls -la alembic/versions/
```

If the files are different, the container and host are using different filesystems.

## Solution

### Option 1: Use a bind mount for development

For local development, Docker Compose can mount the project:

```yaml
services:
  fastapi:
    volumes:
      - .:/app
```

Then:

```text
Host project
     │
     │ bind mount
     ↓
/app inside container
```

Now when Alembic creates:

```bash
alembic revision --autogenerate -m "add users table"
```

the migration file is also created on the host.

For example:

```text
Host:

alembic/versions/
└── 7dda80726bae_add_users_table.py
```

## Option 2: Create migrations from the host

If your host environment can connect to PostgreSQL, you can run Alembic directly from the project:

```bash
alembic revision --autogenerate -m "add users table"
```

and:

```bash
alembic upgrade head
```

This keeps the migration files directly in Git.

## Option 3: Copy a migration out of the container

If you already generated a migration inside the container, copy it to the host:

```bash
sudo docker cp \
  fastapi-app:/app/alembic/versions/7dda80726bae_add_users_table.py \
  ./alembic/versions/
```

Then check:

```bash
git status
```

The migration should now appear as an untracked file.

## Important: Do Not Commit Only the Database Change

A migration has two parts:

```text
SQLAlchemy model
        +
Alembic migration
```

For example:

```text
app/database/models.py
        +
alembic/versions/7dda80726bae_add_users_table.py
```

Both should normally be committed:

```bash
git add app/database/models.py
git add alembic/versions/7dda80726bae_add_users_table.py
git commit -m "feat: add user authentication model"
```

The database itself should not be committed.

## Verify

After creating a migration, check the host:

```bash
ls alembic/versions/
```

Then:

```bash
git status
```

You should see the migration file:

```text
Untracked files:
    alembic/versions/7dda80726bae_add_users_table.py
```

Check the migration history:

```bash
alembic history
```

Then apply it:

```bash
alembic upgrade head
```

Finally check the database:

```bash
alembic current
```

## Lesson

Docker has its own filesystem unless files are shared through a volume or bind mount.

The important distinction is:

```text
COPY . /app
```

means:

> Copy the files into the image.

while:

```yaml
volumes:
  - .:/app
```

means:

> Keep the container's `/app` synchronized with the host project directory.

For development, bind mounts make source-code changes and generated migration files visible on the host.

For production, migrations should normally be treated as version-controlled application artifacts and applied deliberately rather than generated inside a running application container.

The key lesson is:

> **If you generate an Alembic migration inside Docker, make sure `/app` is mounted to your project or copy the migration back to the host before committing it.**
