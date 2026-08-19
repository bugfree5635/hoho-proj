# FastAPI Authentication Dependency Missing

## Problem

When starting the FastAPI application, it fails with an import error:

```text
ModuleNotFoundError: No module named 'passlib'
```

or:

```text
ModuleNotFoundError: No module named 'jose'
```

For example:

```text
File "/app/app/security/auth.py", line 1, in <module>
    from passlib.context import CryptContext

ModuleNotFoundError: No module named 'passlib'
```

Or:

```text
File "/app/app/security/auth.py", line 3, in <module>
    from jose import jwt

ModuleNotFoundError: No module named 'jose'
```

## Cause

The authentication code imports packages that are not installed in the Python environment used by FastAPI.

For example:

```python
from passlib.context import CryptContext
from jose import jwt
```

but the required packages are missing from the environment.

This can happen when:

* the dependency was not added to `requirements.txt`
* the dependency was installed locally but not inside Docker
* the Docker image was built before the dependency was added
* the wrong Python virtual environment is being used
* `requirements.txt` and the actual environment are out of sync

## Solution

Add the required dependencies to `app/requirements.txt`.

For example:

```text
passlib
python-jose[cryptography]
```

Then rebuild the Docker image:

```bash
sudo docker compose build fastapi
```

Restart the application:

```bash
sudo docker compose up -d
```

If the container already exists and you want to rebuild it:

```bash
sudo docker compose up -d --build
```

## Verify

Check that the packages exist inside the container:

```bash
sudo docker exec -it fastapi-app pip list | grep -E "passlib|jose"
```

You can also test the imports directly:

```bash
sudo docker exec -it fastapi-app python -c \
"from passlib.context import CryptContext; from jose import jwt; print('auth dependencies OK')"
```

Then check the application:

```bash
sudo docker logs fastapi-app
```

The FastAPI application should start without the `ModuleNotFoundError`.

## Lesson

Installing a Python package on the host does not automatically install it inside a Docker container.

Think of the environments separately:

```text
Host Python environment
        ≠
Docker Python environment
```

The Docker image gets its dependencies from the Docker build process, usually through:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
```

Therefore, when adding a new Python dependency:

```text
Add dependency
      ↓
requirements.txt
      ↓
Rebuild Docker image
      ↓
Restart container
      ↓
Verify import
```

The key lesson is:

> **A dependency used by the application should be declared in the project's dependency file and installed in the same environment where the application runs.**
