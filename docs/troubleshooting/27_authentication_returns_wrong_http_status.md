# Authentication Returns Wrong HTTP Status

## Problem

An authentication endpoint returns `200 OK` when it should return an error status such as `401 Unauthorized`.

For example, the test expects:

```python
assert response.status_code == 401
```

but receives:

```text
assert 200 == 401
```

The API may also return:

```json
{
  "error": "invalid password"
}
```

with HTTP status `200`.

## Cause

The endpoint returns an error message as a normal response instead of raising a FastAPI `HTTPException`.

For example:

```python
if not verify_password(password, user.hashed_password):
    return {"error": "invalid password"}
```

FastAPI treats this as a successful endpoint execution and therefore returns:

```text
200 OK
```

The response body and HTTP status are separate things:

```text
HTTP status: 200
Body: {"error": "invalid password"}
```

Returning an error-looking JSON object does not automatically make the request an HTTP error.

## Solution

Raise `HTTPException` instead:

```python
from fastapi import HTTPException

if not verify_password(password, user.hashed_password):
    raise HTTPException(
        status_code=401,
        detail="Invalid password",
    )
```

FastAPI will then return:

```text
401 Unauthorized
```

with a response similar to:

```json
{
  "detail": "Invalid password"
}
```

For a user that does not exist:

```python
if not user:
    raise HTTPException(
        status_code=401,
        detail="Invalid username or password",
    )
```

Using the same message for both cases also avoids revealing whether a username exists.

## Debug

First inspect the actual response:

```python
print(response.status_code)
print(response.json())
```

For example:

```text
200
{'error': 'invalid password'}
```

Then check the authentication endpoint.

Look for code like:

```python
return {"error": "..."}
```

inside an error condition.

Replace it with:

```python
raise HTTPException(
    status_code=401,
    detail="...",
)
```

## Test

Create a test for an incorrect password:

```python
def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "henry",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "henry",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
```

Run:

```bash
pytest tests/test_auth.py -v
```

The expected result is:

```text
tests/test_auth.py::test_login_wrong_password PASSED
```

## Verify

Test the API manually:

```bash
curl -X POST localhost/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username": "henry",
  "password": "wrong"
}'
```

Expected:

```text
HTTP/1.1 401 Unauthorized
```

The important part is not just the JSON response.

The HTTP status must correctly communicate the result:

```text
Successful login
        ↓
200 OK

Invalid credentials
        ↓
401 Unauthorized
```

## Lesson

An API communicates the result through both:

```text
HTTP status
+
Response body
```

This:

```python
return {"error": "invalid password"}
```

does **not** mean:

```text
401 Unauthorized
```

It means:

```text
200 OK
{"error": "invalid password"}
```

Use:

```python
raise HTTPException(...)
```

when the request should produce an HTTP error.

The key lesson is:

> **Error information in the response body does not replace the HTTP status code. APIs should use appropriate HTTP status codes to communicate success and failure.**
