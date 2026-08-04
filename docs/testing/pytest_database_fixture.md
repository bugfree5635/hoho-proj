# Pytest Database Fixture

## Overview

This project uses pytest fixtures to provide an isolated database environment for automated tests.

The fixture system is responsible for:

- Creating test database tables
- Replacing the production database dependency
- Providing a FastAPI test client
- Cleaning database state after tests

Testing flow:

```
pytest
   |
   |
pytest fixture
   |
   |
Override application database dependency
   |
   |
Test Database
   |
   |
Run API tests
```

---

# Why Use Fixtures?

Without fixtures, every test needs to manually create:

- Database connection
- Database session
- Test client
- Cleanup logic

Example without fixture:

```python
def test_create_employee():
    db = create_database()
    client = TestClient(app)

    response = client.post(
        "/employees"
    )

    delete_database()
```

Problems:

- Duplicate code
- Easy to forget cleanup
- Tests become difficult to maintain

Pytest fixtures centralize this logic.

---

# Fixture Location

The recommended location:

```
app/
├── tests/
│   ├── conftest.py
│   └── test_api.py
```

`conftest.py` is automatically loaded by pytest.

Tests can use fixtures without importing them.

Example:

```python
def test_create_employee(client):
    response = client.post(
        "/employees"
    )
```

The `client` fixture is automatically available.

---

# Database Configuration

Production database:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

Testing database:

```
SQLite test database
```

Example:

```python
SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./test.db"
)
```

The test database is separated from production data.

---

# Creating Test Database Engine

Example:

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)
```

This creates a SQLAlchemy engine for testing.

Architecture:

```
SQLAlchemy Session
        |
        |
SQLite test.db
```

---

# Creating Test Sessions

Example:

```python
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

The session factory creates database sessions:

```python
db = TestingSessionLocal()
```

Each API request receives a database session.

---

# Database Lifecycle Fixture

Example:

```python
@pytest.fixture(autouse=True)
def setup_database():

    Base.metadata.create_all(
        bind=engine
    )

    yield

    Base.metadata.drop_all(
        bind=engine
    )
```

## Before Test

Tables are created:

```
test.db

employees
---------
(empty)
```

---

## During Test

Test inserts data:

```
employees

id | name
-----------
1  | Henry
```

---

## After Test

Tables are removed:

```
test.db

(empty)
```

Each test starts from a clean state.

---

# Why Use `autouse=True`?

Example:

```python
@pytest.fixture(autouse=True)
def setup_database():
```

`autouse=True` means pytest automatically executes this fixture.

Without it:

```python
def test_api(setup_database):
```

The test must manually request it.

With `autouse=True`:

```python
def test_api():
```

The setup runs automatically.

---

# FastAPI Dependency Override

The application normally uses:

```python
db: Session = Depends(get_database)
```

Production flow:

```
FastAPI
   |
get_database()
   |
PostgreSQL
```

During testing:

```
FastAPI
   |
override_database()
   |
Test Database
```

---

# Override Implementation

Example:

```python
def override_database():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Register override:

```python
app.dependency_overrides[
    get_database
] = override_database
```

Now every API request during testing uses the test database.

---

# Test Client Fixture

Example:

```python
@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app

    return TestClient(app)
```

The client simulates HTTP requests.

Example:

```python
response = client.post(
    "/employees",
    json={
        "name": "Henry",
        "email": "henry@test.com",
        "department": "Security"
    }
)

assert response.status_code == 200
```

Flow:

```
Test Client
    |
HTTP Request
    |
FastAPI Endpoint
    |
Test Database
```

---

# Complete Fixture Flow

When running:

```bash
pytest
```

The process:

```
pytest starts
        |
Load conftest.py
        |
Create test database
        |
Create tables
        |
Override database dependency
        |
Create TestClient
        |
Execute API tests
        |
Cleanup database
        |
Finish
```

---

# CI Integration

GitHub Actions also uses the same idea.

Example:

```
GitHub Runner
      |
Start PostgreSQL service
      |
Install dependencies
      |
Load environment variables
      |
Run pytest
      |
Destroy runner
```

The CI environment is temporary.

Every workflow starts clean.

---

# Common Problems

## Database Dependency Not Overridden

Error:

```
connection refused localhost:5432
```

Cause:

Tests still use production database configuration.

Solution:

Check:

```python
app.dependency_overrides[
    get_database
]
```

---

## Environment Variables Missing

Error:

```
ValidationError:
DATABASE_HOST field required
```

Cause:

Test environment does not provide database variables.

Solution:

Add test variables:

```yaml
env:
  DATABASE_HOST: localhost
  DATABASE_PORT: 5432
```

---

## Test Data Remains

Problem:

```
pytest
pytest
```

Second run fails because duplicate data exists.

Solution:

Use cleanup fixture:

```python
Base.metadata.drop_all()
```

---

# Future Improvement

Current:

```
pytest
    |
SQLite test database
```

Future production-style approach:

```
pytest
    |
Docker PostgreSQL container
    |
Alembic migrations
    |
Integration tests
```

Using the same database engine as production reduces environment differences.

---

# Summary

Pytest fixtures provide a reliable testing environment by:

- Creating isolated database sessions
- Replacing production dependencies
- Providing reusable test clients
- Cleaning state between tests
- Making CI tests repeatable

This design allows the FastAPI application to be tested safely without affecting production data.
