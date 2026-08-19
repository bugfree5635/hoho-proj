# Python Module Not Found

## Problem

The application or test fails with:

```text
ModuleNotFoundError: No module named 'xxx'
```

For example:

```text
ModuleNotFoundError: No module named 'passlib'
```

or:

```text
ModuleNotFoundError: No module named 'jose'
```

The application may work on one machine but fail inside Docker or GitHub Actions.

---

## Cause

Python cannot find the requested package in the current Python environment.

For example:

```python
from passlib.context import CryptContext
```

requires the `passlib` package to be installed.

If it is missing:

```text
Python
  ↓
import passlib
  ↓
package not installed
  ↓
ModuleNotFoundError
```

A common cause is installing the package locally but forgetting to add it to the project's requirements.

---

## Debug

First check which Python is being used:

```bash
which python
```

Check its version:

```bash
python --version
```

Check whether the package is installed:

```bash
pip show passlib
```

or:

```bash
python -m pip show passlib
```

You can also test the import directly:

```bash
python -c "import passlib; print(passlib.__version__)"
```

If it is not installed, you may see:

```text
WARNING: Package(s) not found: passlib
```

---

## Check the Environment

A very common problem is using the wrong Python environment.

For example:

```bash
which python
```

might show:

```text
/home/henry/practice/hoho-proj/.venv/bin/python
```

but Docker uses:

```text
/usr/local/bin/python
```

These are different environments.

Installing a package into `.venv` does not install it into the Docker container.

Think of them as separate:

```text
Local machine
└── .venv
    └── passlib

Docker container
└── Python
    └── passlib missing
```

---

## Solution

Install the missing package into the current environment:

```bash
python -m pip install passlib
```

For example:

```bash
python -m pip install python-jose
```

However, installing it manually is not enough for a reproducible project.

Add the dependency to your requirements file.

For example:

```text
passlib
python-jose[cryptography]
```

Then rebuild/install the environment:

```bash
pip install -r requirements.txt
```

---

## Docker

If the application runs inside Docker, installing the package on your host does not fix the container.

For example, this:

```bash
pip install passlib
```

on your host does **not** automatically install `passlib` inside:

```text
fastapi-app
```

Make sure the package exists in:

```text
requirements.txt
```

Then rebuild the image:

```bash
docker compose build
```

or:

```bash
docker compose up --build
```

After rebuilding, verify inside the container:

```bash
docker exec -it fastapi-app python -m pip show passlib
```

You can also test:

```bash
docker exec -it fastapi-app \
python -c "import passlib; print('passlib OK')"
```

---

## GitHub Actions

The same problem can happen in CI.

Your local environment might contain:

```text
passlib
python-jose
```

while GitHub Actions installs only:

```bash
pip install -r requirements.txt
```

If the dependency isn't listed there, CI will fail:

```text
ModuleNotFoundError: No module named 'passlib'
```

The solution is to declare the dependency in the project's dependency file.

For example:

```text
# requirements.txt

fastapi
sqlalchemy
psycopg
passlib
python-jose[cryptography]
```

Then GitHub Actions can recreate the environment:

```text
GitHub Actions
      ↓
pip install -r requirements.txt
      ↓
all declared dependencies
      ↓
pytest
```

---

## `pip` vs `python -m pip`

Prefer:

```bash
python -m pip install package
```

instead of:

```bash
pip install package
```

because it makes it clearer which Python installation receives the package.

For example:

```bash
python -m pip install passlib
```

means:

```text
this Python
    ↓
this Python's pip
    ↓
install passlib
```

This helps avoid situations where:

```bash
pip
```

belongs to one Python installation while:

```bash
python
```

belongs to another.

---

## Check the Import Name

The package name and Python import name are not always identical.

For example:

```text
Package:
python-jose

Import:
jose
```

So this is correct:

```bash
pip install python-jose
```

and:

```python
from jose import jwt
```

Similarly:

```text
Package:
passlib

Import:
passlib
```

so:

```bash
pip install passlib
```

and:

```python
from passlib.context import CryptContext
```

---

## Common Mistake

Do not solve the problem only by doing:

```bash
pip install missing-package
```

and then forget the requirements file.

It may appear fixed locally:

```text
Local machine
    ↓
pip install
    ↓
works
```

but another environment will fail:

```text
Docker
    ↓
requirements.txt
    ↓
package missing
    ↓
ModuleNotFoundError
```

The dependency should be declared in the project.

---

## Verify

After installing the dependency:

```bash
python -c "import passlib; print('OK')"
```

Then run the application:

```bash
uvicorn app.main:app --reload
```

For Docker:

```bash
docker compose up --build
```

For tests:

```bash
pytest
```

For GitHub Actions, push the dependency change and verify the CI workflow.

---

## Troubleshooting Checklist

When you see:

```text
ModuleNotFoundError: No module named 'xxx'
```

check these in order:

```text
1. What module is missing?
       ↓
2. Which Python am I using?
       ↓
   which python
       ↓
3. Is the package installed?
       ↓
   python -m pip show xxx
       ↓
4. Is the dependency declared?
       ↓
   requirements.txt / pyproject.toml
       ↓
5. Am I running inside Docker?
       ↓
   install/rebuild the container
       ↓
6. Am I running in GitHub Actions?
       ↓
   make sure CI installs the dependency
```

---

## Lesson

A Python dependency is not just something you install once on your computer.

A reliable project needs to **declare its dependencies** so that every environment can recreate them.

```text
Code
 ↓
requirements.txt / pyproject.toml
 ↓
Docker / CI / local environment
 ↓
same dependencies
 ↓
same application
```

The key lesson is:

> **If your code imports a third-party package, make that dependency explicit in the project's dependency configuration. Installing it manually only fixes the current environment.**
