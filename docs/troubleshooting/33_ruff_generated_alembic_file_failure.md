# Ruff Generated Alembic File Failure

## Problem

Ruff fails during CI or local linting because an automatically generated Alembic migration file does not follow the project's formatting or linting rules.

For example:

```text
alembic/versions/7dda80726bae_add_users_table.py
```

may contain generated code such as:

```python
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
```

and Ruff reports errors such as:

```text
F401 `sqlalchemy as sa` imported but unused
E501 Line too long
```

The application itself may work correctly and the migration may execute successfully:

```bash
alembic upgrade head
```

but CI still fails during linting.

---

## Cause

Alembic generates migration files automatically.

For example:

```bash
alembic revision --autogenerate -m "add users table"
```

creates:

```text
alembic/
└── versions/
    └── 7dda80726bae_add_users_table.py
```

The generated file is intended to be edited by Alembic developers, but it does not necessarily match every Ruff rule configured in the project.

Therefore:

```text
Alembic
   ↓
generates migration
   ↓
Ruff checks migration
   ↓
Ruff finds lint violations
   ↓
CI fails
```

This is especially common when Ruff is configured to lint the entire repository:

```text
app/
tests/
alembic/
```

---

## Debug

Run Ruff locally:

```bash
ruff check .
```

To check only the migration:

```bash
ruff check alembic/versions/7dda80726bae_add_users_table.py
```

To see formatting problems:

```bash
ruff format --check .
```

You can also ask Ruff to automatically fix safe issues:

```bash
ruff check . --fix
```

and format the files:

```bash
ruff format .
```

However, do not blindly apply automatic fixes to migration files without reviewing the result.

---

## Check the Generated Migration

Open the migration:

```bash
cat alembic/versions/7dda80726bae_add_users_table.py
```

A typical Alembic migration looks like:

```python
"""add users table"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7dda80726bae"
down_revision: Union[str, Sequence[str], None] = "4838c302a2a5"


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
```

The `sa` import is actually required by the migration:

```python
sa.Column(...)
sa.Integer()
sa.String()
```

So if Ruff reports it as unused, check the exact generated file before removing it.

---

## Solution 1: Format the Migration

If the problem is formatting, run:

```bash
ruff format alembic/versions/
```

Then check again:

```bash
ruff check alembic/versions/
```

This is usually the simplest solution.

---

## Solution 2: Fix the Specific Ruff Error

If Ruff reports a specific issue:

```text
F401 ...
```

inspect whether the import is actually needed.

For example:

```python
import sqlalchemy as sa
```

is needed if the migration contains:

```python
sa.Column(...)
sa.String()
sa.Integer()
```

Do not remove it simply because Ruff reports an import problem without checking the generated code.

---

## Solution 3: Exclude Alembic Migrations

Migration files are generated infrastructure code and some teams choose not to apply normal application linting rules to them.

For example, in `pyproject.toml`:

```toml
[tool.ruff]
exclude = [
    "alembic/versions/",
]
```

Then:

```bash
ruff check .
```

will skip generated migration files.

This can be a reasonable choice if Alembic owns the structure of those files.

---

## Solution 4: Exclude Only Generated Migration Files

If you still want Ruff to check the rest of the Alembic directory, you can exclude only:

```text
alembic/versions/
```

while continuing to lint:

```text
alembic/env.py
```

For example:

```toml
[tool.ruff]
exclude = [
    "alembic/versions/",
]
```

This gives you:

```text
alembic/env.py
      ↓
Ruff checks it

alembic/versions/*.py
      ↓
Ruff ignores generated migrations
```

---

## Solution 5: Use Per-File Ignores

If you only need to ignore a specific Ruff rule for migration files:

```toml
[tool.ruff.lint.per-file-ignores]
"alembic/versions/*.py" = ["E501"]
```

For multiple rules:

```toml
[tool.ruff.lint.per-file-ignores]
"alembic/versions/*.py" = ["E501", "F401"]
```

Only use the rules that are actually necessary.

Do not disable all Ruff checking unless you have a reason.

---

## Check Your Ruff Configuration

Look at:

```bash
cat pyproject.toml
```

You may have something like:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F"]
```

This means Ruff checks the repository using the configured rules.

If Alembic migrations are included in the repository, Ruff may inspect them too.

---

## Why Alembic Files Are Different

Application code is normally written manually:

```text
app/
├── api/
├── security/
├── database/
└── schemas/
```

Migration code is often generated:

```text
alembic/
└── versions/
    ├── 001_initial.py
    ├── 002_add_users.py
    └── 003_add_tokens.py
```

These files have a different purpose.

Their most important requirements are:

```text
Correct migration
        ↓
Correct upgrade()
        ↓
Correct downgrade()
        ↓
Correct revision chain
```

Formatting is secondary.

---

## Important: Never Delete a Migration Just to Fix Ruff

Do not do this:

```bash
rm alembic/versions/7dda80726bae_add_users_table.py
```

simply because Ruff reports an error.

The migration may already be part of the database migration history.

Before modifying or deleting a migration, check:

```bash
alembic history
```

and:

```bash
alembic current
```

Also check:

```bash
git status
```

If the migration has already been committed or used by another environment, deleting it can break the migration chain.

---

## Verify

After fixing the problem:

```bash
ruff check .
```

Then:

```bash
ruff format --check .
```

Then verify the migration itself:

```bash
alembic upgrade head
```

Finally run:

```bash
pytest
```

Your CI pipeline should then look like:

```text
Ruff
 ↓
Alembic
 ↓
Pytest
 ↓
Coverage
 ↓
GitHub Actions
```

---

## Lesson

Alembic migration files are **generated database infrastructure code**, not ordinary application code.

When Ruff reports a problem in a generated migration, first determine whether:

1. the migration actually contains a real lint problem;
2. Ruff's formatting can safely fix it;
3. the migration directory should be excluded from normal linting.

A useful project configuration is often:

```text
Application code
    ↓
Ruff checks strictly

Tests
    ↓
Ruff checks

Alembic configuration
    ↓
Ruff checks

Generated migration files
    ↓
Optional exclusion
```

The key lesson is:

> **Don't change database migration logic just to satisfy a linter. First understand whether the warning comes from generated code, then either safely format/fix it or configure Ruff appropriately for generated migrations.**
