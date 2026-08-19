# Passlib Bcrypt Backend Compatibility

## Problem

When registering a user, password hashing fails even though `passlib` is installed correctly.

The application returns an error similar to:

```text
ValueError: password cannot be longer than 72 bytes,
truncate manually if necessary
```

The traceback points to:

```text
passlib/handlers/bcrypt.py
```

For example:

```text
File ".../passlib/handlers/bcrypt.py", line 626, in _load_backend_mixin
    return mixin_cls._finalize_backend_mixin(name, dryrun)

File ".../passlib/handlers/bcrypt.py", line 380, in detect_wrap_bug
    if verify(secret, bug_hash):

ValueError: password cannot be longer than 72 bytes
```

## Cause

The problem is caused by a compatibility issue between the version of `passlib` being used and the installed `bcrypt` backend.

`passlib` uses the `bcrypt` package to perform password hashing:

```text
FastAPI
   ↓
Passlib
   ↓
bcrypt
   ↓
password hash
```

When Passlib initializes the bcrypt backend, it performs an internal compatibility check.

With newer versions of `bcrypt`, this check can fail because the bcrypt backend enforces its 72-byte password limit differently.

This means the error can appear even when the actual password supplied by the user is short.

For example:

```text
password = "123456"
```

is nowhere near 72 bytes, but Passlib's internal backend detection can still trigger the error.

## Debug

Check the installed versions:

```bash
pip show passlib
pip show bcrypt
```

Or:

```bash
pip list | grep -E "passlib|bcrypt"
```

Inside Docker:

```bash
sudo docker exec -it fastapi-app \
pip list | grep -E "passlib|bcrypt"
```

Test bcrypt directly:

```bash
python -c "import bcrypt; print(bcrypt.__version__)"
```

Then test Passlib:

```bash
python -c \
"from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']))"
```

If the Passlib initialization triggers the same error, the problem is with the Passlib/bcrypt backend combination rather than the FastAPI endpoint.

## Solution

One solution is to use a bcrypt version compatible with the Passlib version used by the project.

For example, pin the dependency:

```text
passlib==1.7.4
bcrypt==4.0.1
```

Then reinstall:

```bash
pip install -r requirements.txt
```

For Docker, rebuild the image:

```bash
sudo docker compose up -d --build
```

Then verify:

```bash
sudo docker exec -it fastapi-app \
pip list | grep -E "passlib|bcrypt"
```

Test password hashing again:

```bash
sudo docker exec -it fastapi-app python -c \
"from passlib.context import CryptContext; \
ctx=CryptContext(schemes=['bcrypt']); \
print(ctx.hash('123456'))"
```

A bcrypt hash should be returned:

```text
$2b$12$...
```

## Verify

Start the application:

```bash
sudo docker logs fastapi-app
```

Then test registration:

```bash
curl -X POST localhost/auth/register \
-H "Content-Type: application/json" \
-d '{
  "username": "henry",
  "password": "123456"
}'
```

The registration should complete without the Passlib/bcrypt backend error.

Then test login:

```bash
curl -X POST localhost/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username": "henry",
  "password": "123456"
}'
```

A successful login should return an access token:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Test an incorrect password as well:

```bash
curl -X POST localhost/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username": "henry",
  "password": "wrong"
}'
```

The API should reject the login rather than returning a valid token.

## Improvement

For a new application, consider whether Passlib is the best password-hashing dependency for the project.

Password hashing should use a maintained and well-supported implementation, and dependency versions should be pinned and tested in CI.

For example:

```text
requirements.txt
```

should explicitly declare the versions used by the application rather than relying on whatever happens to be installed:

```text
passlib==1.7.4
bcrypt==4.0.1
```

This makes the Docker build and CI environment reproducible.

## Lesson

A Python dependency is not always isolated from the behavior of another dependency.

In this case:

```text
Passlib
   ↓
bcrypt backend
   ↓
Python package version
```

all affect password hashing.

The important lesson is:

> **When a library fails inside one of its backend implementations, check the versions of the library and its backend dependency before changing your application code.**
