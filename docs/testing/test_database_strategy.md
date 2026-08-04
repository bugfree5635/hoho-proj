# Test Database Strategy

## Overview

This project uses an isolated database strategy for automated testing.

The purpose is to ensure:

- Tests never modify production data
- Every test starts from a predictable state
- Database-related bugs can be detected
- CI pipelines produce reliable results

Testing architecture:

```
Developer
    |
    |
pytest
    |
    |
Test Database
    |
    |
Database Engine
```

---

# Why Use a Separate Test Database?

The application uses PostgreSQL as the production database.

Production database:

```
company
```

Testing should never connect directly to:

```
company
```

because tests may:

- Insert temporary data
- Modify existing records
- Delete tables
- Change database schema

Example of a bad design:

```
pytest
    |
    |
Production Database
    |
    |
company
```

Problems:

- Production data can be damaged
- Tests become dangerous
- CI execution becomes unpredictable

---

# Isolated Test Environment

The preferred design:

```
pytest
    |
    |
Test Database
    |
    |
company_test
```

The test database contains only temporary data.

Example:

```
company_test

employees table

id | name
---------
1  | Test User
```

After testing:

```
company_test

(empty)
```

Production remains unchanged:

```
company

real users
real employees
real data
```

---

# Database Lifecycle

Each test execution follows the same lifecycle:

```
Start Test Environment
          |
          |
Create Database Tables
          |
          |
Execute Tests
          |
          |
Remove Test Data
          |
          |
Finish
```

The goal is:

```
Same test
+
Same environment
=
Same result
```

---

# Production Database vs Test Database

## Production

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

Used by:

```
Application Container
        |
        |
PostgreSQL Database
```

---

## Testing

Example:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=company_test
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

Used by:

```
pytest
    |
    |
Test Database
```

---

# Testing Approaches

There are several ways to isolate database tests.

---

## Option 1: Separate Database

Example:

```
company

Production

company_test

Testing
```

Advantages:

- Similar to production
- Real database behavior
- Easy to understand

Disadvantages:

- Requires database management
- Cleanup is required

This project follows this strategy.

---

## Option 2: SQLite Test Database

Example:

```python
DATABASE_URL = (
    "sqlite:///./test.db"
)
```

Architecture:

```
pytest
    |
    |
SQLite
    |
    |
test.db
```

Advantages:

- Fast
- Simple setup
- No database server required

Disadvantages:

- SQLite behavior differs from PostgreSQL
- Some PostgreSQL features cannot be tested

Useful for:

- Unit tests
- Simple API tests

---

## Option 3: Temporary Database Container

Example:

```
pytest
    |
Docker PostgreSQL Container
    |
Temporary Database
```

Advantages:

- Same database engine as production
- Clean environment
- Good for CI

Disadvantages:

- More setup complexity

This is commonly used in production environments.

---

# Database Cleanup Strategy

Tests should not depend on previous test results.

Bad:

```
Test 1
creates employee
Database:
Employee A


Test 2
expects empty database
Failure
```

Good:

```
Test 1
Create data
Cleanup


Test 2
New clean database
Create data
Cleanup
```

---

# Why Not Manually Delete Data?

Example:

```python
db.query(Employee).delete()
```

This approach becomes difficult when relationships increase.

Example:

```
Employee
    |
    |
Department
    |
    |
Permission
```

Cleaning requires understanding every relationship.

Better:

```
Create fresh database

Run tests

Destroy database
```

---

# Why Not Use Random Test Data?

Example:

```python
email = uuid.uuid4()
```

Result:

```
abc123@test.com

xyz456@test.com
```

Advantages:

- Avoid duplicate errors

Disadvantages:

- May hide database constraint problems
- Tests do not represent real scenarios

Example:

A unique constraint bug may never appear.

Therefore:

```
Clean database
+
Fixed test data
```

is usually preferred.

---

# CI Pipeline Integration

GitHub Actions creates a temporary testing environment.

Flow:

```
GitHub Actions Runner
          |
          |
Start PostgreSQL Service
          |
          |
Install Dependencies
          |
          |
Set Environment Variables
          |
          |
Run pytest
          |
          |
Destroy Runner
```

Every CI execution starts from zero.

---

# Database Dependency Override

The application normally uses:

```python
db = Depends(get_database)
```

Production:

```
FastAPI
   |
get_database()
   |
PostgreSQL
```

Testing:

```
FastAPI
   |
override_database()
   |
Test Database
```

This prevents tests from accessing production resources.

---

# Migration Strategy

Current approach:

```python
Base.metadata.create_all()
```

This is acceptable for development and testing.

Future production approach:

```
pytest
    |
Alembic migration
    |
PostgreSQL database
```

Example:

```bash
alembic upgrade head
```

Benefits:

- Version controlled schema
- Repeatable deployments
- Safer database changes

---

# Current Project Design

Current:

```
FastAPI
    |
SQLAlchemy
    |
Test Database
    |
pytest
```

CI:

```
GitHub Actions
    |
PostgreSQL Service
    |
pytest
    |
Result
```

---

# Summary

The project uses an isolated database testing strategy:

- Production data is protected
- Tests use a separate database
- Database state is predictable
- CI runs in a clean environment
- Tests can execute repeatedly

A separate test database provides a safer foundation for automated testing and continuous integration.
