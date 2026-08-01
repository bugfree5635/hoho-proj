# Python Dependency Compatibility Issue

## Problem

While running automated tests:

```bash
pytest
```

the test execution was successful, but a dependency compatibility warning appeared:

```
StarletteDeprecationWarning:

Using httpx with starlette.testclient is deprecated;
install httpx2 instead.
```

The test result:

```
1 passed, 1 warning
```

The application worked correctly, but the dependency versions were not fully compatible.

---

# Environment

Development environment:

```
Ubuntu Linux
 |
Python 3.14.4
 |
FastAPI
 |
Starlette
 |
Pytest
 |
HTTP Client Testing Library
```

Project:

```
hoho-proj

├── app
│   ├── main.py
│   ├── tests
│   │   └── test_api.py
│   └── requirements.txt
```

---

# Investigation

## Check Installed Packages

Checked dependency versions:

```bash
pip show fastapi starlette httpx
```

The FastAPI testing framework uses:

```
FastAPI
    |
    |
Starlette TestClient
    |
    |
HTTP client library
```

A version mismatch between these packages caused the warning.

---

# Root Cause Analysis

The application code was correct.

The problem was caused by dependency compatibility.

Modern Python applications depend on many external packages:

```
Application Code

       |
       |

FastAPI

       |
       |

Starlette

       |
       |

HTTP Client

       |
       |

Python Runtime
```

When one package changes its API or dependency requirements,
older versions may generate warnings or fail.

---

# Solution

## Install Required Dependency

Installed the compatible HTTP client package:

```bash
pip install httpx2
```

---

## Update Requirements

After fixing the environment:

```bash
pip freeze > requirements.txt
```

This records the working dependency versions.

Example:

```
fastapi
uvicorn
sqlalchemy
pydantic
pydantic-settings
psycopg
pytest
httpx2
```

---

# Verification

Run tests again:

```bash
pytest
```

Expected result:

```
============================= test session starts =============================

app/tests/test_api.py .                         [100%]

============================== 1 passed ================================
```

The API test environment was working correctly.

---

# Lessons Learned

## 1. Dependency management is part of system administration

Application reliability depends on:

* correct package versions
* reproducible environments
* dependency updates

---

## 2. Always check warnings

Warnings may indicate future failures.

A warning today can become:

```
working system
        |
        |
future package update
        |
        |
application failure
```

---

## 3. Maintain reproducible environments

Best practices:

```bash
python -m venv .venv

pip install -r requirements.txt

pip freeze > requirements.txt
```

This allows another engineer to recreate the same environment.

---

## 4. Troubleshooting Method

When dependency problems happen:

1. Read the error message

2. Check installed versions:

```bash
pip list
```

3. Check package relationships:

```bash
pip show package_name
```

4. Update or pin versions

5. Run tests again

---

# Final Result

Before:

```
pytest

1 passed
1 warning
```

After dependency adjustment:

```
pytest

1 passed
0 warnings
```

The project now has a reproducible Python testing environment suitable for deployment workflows.


