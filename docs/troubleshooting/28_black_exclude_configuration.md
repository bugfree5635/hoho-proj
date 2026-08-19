# Black Exclude Configuration

## Problem

Black checks the formatting of the whole project:

```bash
black --check .
```

and fails because some files are not formatted:

```text
would reformat test_db.py
would reformat alembic/env.py
would reformat alembic/versions/4838c302a2a5_initial_migration.py

Oh no! 💥 💔 💥
3 files would be reformatted
```

However, you may not want Black to manage certain files or directories.

For example:

```text
alembic/
```

may contain generated migration files that you do not want Black to automatically modify.

## Cause

Black recursively checks Python files under the specified directory.

When running:

```bash
black --check .
```

Black searches the project and finds Python files such as:

```text
app/
tests/
alembic/
```

If one of those files does not match Black's formatting rules, CI fails.

## Solution

Configure Black's `exclude` option in `pyproject.toml`.

For example:

```toml
[tool.black]
line-length = 88
exclude = '''
/(
    alembic
)/
'''
```

Now Black will ignore the `alembic` directory.

Your project might look like:

```text
hoho-proj/
├── app/
├── tests/
├── alembic/
├── pyproject.toml
└── ...
```

Black will check:

```text
app/
tests/
```

but skip:

```text
alembic/
```

## Exclude Specific Files

If you only want to exclude one file:

```toml
[tool.black]
exclude = '''
/(
    alembic/versions/4838c302a2a5_initial_migration\.py
)/
'''
```

However, excluding the entire `alembic/` directory is usually simpler if the migration files are generated and you intentionally do not want Black to manage them.

## Multiple Exclusions

You can exclude multiple directories:

```toml
[tool.black]
line-length = 88
exclude = '''
/(
    alembic
  | migrations
  | generated
)/
'''
```

This tells Black to skip:

```text
alembic/
migrations/
generated/
```

## Verify

Run:

```bash
black --check .
```

Black should no longer report files inside the excluded directory.

You can also check what Black would format:

```bash
black --check --verbose .
```

The verbose output helps confirm that the exclusion is being applied.

## Important: Black and Ruff Are Separate

Configuring Black does **not** automatically configure Ruff.

For example:

```toml
[tool.black]
exclude = '''
/(
    alembic
)/
'''
```

only affects:

```bash
black
```

Ruff has its own configuration.

If Ruff also checks the migration files:

```bash
ruff check .
```

configure Ruff separately:

```toml
[tool.ruff]
exclude = [
    "alembic",
]
```

Depending on your Ruff version/configuration, you may instead use the appropriate `lint` configuration section.

The important idea is:

```text
Black configuration
        ↓
controls Black

Ruff configuration
        ↓
controls Ruff
```

## CI

If your GitHub Actions workflow contains:

```yaml
- name: Check formatting
  run: black --check .
```

the same `pyproject.toml` configuration is used in CI.

You do not need to change the GitHub Actions command.

For example:

```text
Local
    ↓
black --check .
    ↓
pyproject.toml
    ↓
alembic excluded

GitHub Actions
    ↓
black --check .
    ↓
same pyproject.toml
    ↓
alembic excluded
```

## Alternative

Instead of excluding Alembic entirely, you can format the files:

```bash
black alembic/
```

This is often preferable if you want all Python code in the repository to follow the same formatting standard.

Generated Alembic migrations are still Python code, and Black can format them without changing their database behavior.

Therefore, consider whether you actually need the exclusion.

## Lesson

Black is a project-wide formatter when you run:

```bash
black --check .
```

You can control what it checks through `pyproject.toml`.

The key lesson is:

> **Use Black's `exclude` configuration when certain generated or intentionally unmanaged files should not participate in the project's formatting check.**

Also remember that **Black and Ruff are independent tools**. If both run in CI, configure each tool according to your project's needs.
