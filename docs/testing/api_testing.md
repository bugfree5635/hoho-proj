Based on your portfolio goal (**Linux Sysadmin / DevOps Engineer**), these two documents should not just explain "how to call API". They should show:

* how an engineer verifies deployment
* how an engineer tests service availability
* how an engineer troubleshoots failures
* how application + database + Docker work together

# API Testing Documentation

## Overview

This document describes how to verify the Employee Management API after deployment.

Testing methods simulate real operations performed by:

- Developers
- QA engineers
- System administrators
- DevOps engineers


Application architecture:

```

Client
|
|
HTTP Request
|
|
FastAPI Application
|
|
SQLAlchemy
|
|
PostgreSQL Database

```

---

# Environment

Development environment:

```

Ubuntu Server

FastAPI
localhost:8000

PostgreSQL
localhost:5432

Docker Container
postgres:16

```

---

# 1. Health Check Testing

## Purpose

Verify that the application service is running correctly.

Endpoint:

```

GET /health

```

Command:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
    "status": "ok"
}
```

Successful result means:

* FastAPI process is running
* Application can receive HTTP requests

---

# 2. Swagger API Testing

FastAPI provides automatic API documentation.

Open:

```
http://localhost:8000/docs
```

Swagger UI allows testing:

* GET requests
* POST requests
* Request parameters
* Response data

---

# 3. Create Employee API Test

## Endpoint

```
POST /employees
```

## Request Body

```json
{
    "name": "Henry",
    "email": "henry@example.com",
    "department": "IT"
}
```

---

## Method 1: Swagger UI

Steps:

1. Open:

```
http://localhost:8000/docs
```

2. Select:

```
POST /employees
```

3. Click:

```
Try it out
```

4. Enter JSON:

```json
{
    "name": "Henry",
    "email": "henry@example.com",
    "department": "IT"
}
```

5. Click:

```
Execute
```

Expected:

HTTP Status:

```
200 OK
```

Response:

```json
{
    "id":1,
    "name":"Henry",
    "email":"henry@example.com",
    "department":"IT"
}
```

---

# 4. Command Line Testing Using curl

## Create Employee

Command:

```bash
curl -X POST http://localhost:8000/employees \
-H "Content-Type: application/json" \
-d '
{
    "name":"Henry",
    "email":"henry@example.com",
    "department":"IT"
}'
```

Expected:

```json
{
    "id":1,
    "name":"Henry",
    "email":"henry@example.com",
    "department":"IT"
}
```

---

# 5. Database Verification

After creating an employee, verify data exists in PostgreSQL.

Enter database:

```bash
docker exec -it postgres psql \
-U admin \
-d company
```

Check table:

```sql
SELECT * FROM employees;
```

Expected:

```
id | name  | email              | department
---+-------+--------------------+------------
1  | Henry | henry@example.com  | IT
```

This verifies:

```
API
 |
SQLAlchemy
 |
PostgreSQL
```

working correctly.

---

# 6. Automated API Testing

Location:

```
app/tests/test_api.py
```

Example:

```python
def test_create_employee():

    response = client.post(
        "/employees",
        json={
            "name":"Henry",
            "email":"henry@example.com",
            "department":"IT"
        }
    )

    assert response.status_code == 200
```

Run:

```bash
pytest
```

Expected:

```
1 passed
```

---

# 7. Troubleshooting

## API returns 404

Example:

```
GET /
404 Not Found
```

Cause:

The endpoint does not exist.

Solution:

Check available routes:

```
http://localhost:8000/docs
```

---

## Database connection failure

Example:

```
failed to resolve host 'postgres'
```

Possible causes:

* wrong database hostname
* PostgreSQL container stopped
* wrong Docker network

Detailed document:

```
docs/troubleshooting/01_postgresql_hostname_resolution_failure.md
```

---

# Testing Checklist

| Test            | Expected Result             |
| --------------- | --------------------------- |
| FastAPI startup | Service starts successfully |
| Health check    | status=ok                   |
| Swagger access  | Documentation available     |
| POST employee   | Employee created            |
| Database query  | Data stored correctly       |
| Automated tests | pytest passed               |

---

# Skills Demonstrated

* REST API testing
* Linux command line troubleshooting
* Database verification
* Docker service validation
* Application health checking
* Basic CI/CD testing concepts
