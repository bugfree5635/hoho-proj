# GitHub Actions Docker Image Build Failure

## Problem

GitHub Actions fails while building the Docker image.

For example:

```text
ERROR: failed to solve: ...
```

or:

```text
failed to fetch anonymous token
```

or:

```text
failed to build
```

The application may build successfully on the local machine but fail inside GitHub Actions.

---

## Cause

Docker image building depends on several external components:

```text
GitHub Actions
      ↓
Docker Build
      ↓
Dockerfile
      ↓
Base image
      ↓
Docker Hub / Registry
      ↓
Python dependencies
      ↓
Application
```

A failure at any stage can stop the build.

Common causes include:

* invalid Dockerfile syntax
* incorrect build context
* missing files
* incorrect `COPY` paths
* unavailable Docker registry
* Docker Hub rate limiting
* dependency installation failure
* incorrect Python version
* network failure
* Docker Compose configuration problems

---

## Debug

First inspect the GitHub Actions log.

Look for the **first actual error**, not necessarily the final error.

For example:

```text
ERROR: failed to fetch anonymous token
```

is more useful than:

```text
Process completed with exit code 1
```

The final line only tells you that the workflow failed.

---

## Test the Docker Build Locally

Run:

```bash
docker build -t hoho-proj .
```

If you use Docker Compose:

```bash
docker compose build
```

Or:

```bash
docker compose up -d --build
```

If the local build also fails, the problem is probably in the Docker configuration or application.

If:

```text
Local build
    ↓
works

GitHub Actions
    ↓
fails
```

then investigate the CI environment, registry access, secrets, networking, or build context.

---

## Check the Dockerfile

A typical FastAPI Dockerfile might look like:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Check each step:

```text
FROM
 ↓
WORKDIR
 ↓
COPY requirements.txt
 ↓
pip install
 ↓
COPY application
 ↓
start FastAPI
```

---

## Check the Build Context

A common mistake is running:

```bash
docker build .
```

from the wrong directory.

For example:

```text
hoho-proj/
├── Dockerfile
├── requirements.txt
├── app/
└── tests/
```

The build should normally be executed from:

```bash
cd ~/practice/hoho-proj
```

then:

```bash
docker build -t hoho-proj .
```

The final `.` means:

> Use the current directory as the Docker build context.

---

## `COPY` Problems

Suppose the Dockerfile contains:

```dockerfile
COPY requirements.txt .
```

Docker expects:

```text
build-context/
└── requirements.txt
```

If the file isn't inside the build context, Docker cannot copy it.

You may see:

```text
COPY failed
```

or:

```text
"/requirements.txt": not found
```

Check:

```bash
ls
```

and:

```bash
ls requirements.txt
```

---

## Docker Hub / Base Image Failure

If the Dockerfile contains:

```dockerfile
FROM python:3.14-slim
```

Docker needs to download the Python base image.

GitHub Actions therefore needs access to the container registry.

A failure might look like:

```text
failed to fetch anonymous token
```

or:

```text
failed to resolve source metadata
```

This can indicate:

* registry/network problems
* temporary Docker Hub problems
* rate limiting
* DNS problems

Try locally:

```bash
docker pull python:3.14-slim
```

If that also fails, the problem may not be your application.

---

## Dependency Installation Failure

Another common failure happens here:

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

For example:

```text
ERROR: Could not find a version that satisfies the requirement ...
```

Check your requirements:

```bash
cat requirements.txt
```

Then test locally:

```bash
python -m pip install -r requirements.txt
```

For your FastAPI application, make sure dependencies used by the code are declared.

For example:

```text
fastapi
uvicorn
sqlalchemy
psycopg
passlib
python-jose[cryptography]
```

The exact list depends on your project.

---

## Python Version Compatibility

Check your Docker image:

```dockerfile
FROM python:3.14-slim
```

and your local Python:

```bash
python --version
```

and CI Python version if your workflow also runs tests directly.

For example:

```text
Local:
Python 3.14

Docker:
Python 3.14

GitHub Actions:
Python 3.14
```

Keeping versions aligned reduces environment-specific failures.

---

## GitHub Actions Example

A simple Docker build workflow might contain:

```yaml
name: Docker Build

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t hoho-proj .
```

The important part is:

```yaml
uses: actions/checkout@v4
```

Without checking out the repository, the runner does not have your Dockerfile or application source code.

---

## Docker Compose in GitHub Actions

If your project uses Compose:

```yaml
- name: Build services
  run: docker compose build
```

or:

```yaml
- name: Start services
  run: docker compose up -d --build
```

Make sure the Compose file exists:

```bash
ls compose.yml
```

or:

```bash
ls docker-compose.yml
```

Also verify the paths used by `build:`.

For example:

```yaml
services:
  fastapi:
    build:
      context: .
      dockerfile: Dockerfile
```

Here:

```text
context: .
```

means the repository root is the build context.

---

## `.dockerignore`

Check whether `.dockerignore` accidentally excludes required files.

For example:

```text
.venv/
.git/
__pycache__/
```

is reasonable.

But if you have:

```text
app/
```

in `.dockerignore`, Docker may not copy your application.

For example:

```dockerfile
COPY . .
```

would then exclude:

```text
app/
```

and the container might later fail with:

```text
ModuleNotFoundError
```

Check:

```bash
cat .dockerignore
```

---

## Build Without Cache

Sometimes you need to determine whether an old cached layer is hiding the problem.

Run:

```bash
docker build --no-cache -t hoho-proj .
```

For Compose:

```bash
docker compose build --no-cache
```

If the clean build succeeds, the problem may have involved a cached layer.

---

## Verify the Image

After building:

```bash
docker images
```

You should see:

```text
hoho-proj
```

Run it:

```bash
docker run --rm -p 8000:8000 hoho-proj
```

Then test:

```bash
curl http://localhost:8000/health
```

If your application returns:

```json
{"status":"ok"}
```

the image can start successfully.

---

## Common Mistake

Do not immediately change the GitHub Actions workflow when the Docker build fails.

First determine where the failure occurs:

```text
Dockerfile parsing?
        ↓
Base image?
        ↓
COPY?
        ↓
pip install?
        ↓
application files?
        ↓
container startup?
```

For example:

```text
Docker build failure
```

is different from:

```text
Container startup failure
```

A successful image build does not guarantee that the application starts.

---

## Debugging Checklist

Run these locally:

```bash
docker build -t hoho-proj .
```

```bash
docker compose build
```

```bash
docker compose up -d --build
```

```bash
docker compose ps
```

```bash
docker compose logs fastapi
```

Check the repository:

```bash
git status
```

Check Docker files:

```bash
cat Dockerfile
cat compose.yml
cat .dockerignore
```

Check dependencies:

```bash
cat requirements.txt
```

---

## Lesson

A Docker build is an independent environment.

Your local environment might contain:

```text
Python
packages
environment variables
Docker cache
credentials
```

while GitHub Actions starts with a clean runner.

Therefore:

```text
Works on my machine
        ≠
Works in CI
```

A good CI pipeline should reproduce the application from the repository itself:

```text
GitHub repository
       ↓
Dockerfile
       ↓
requirements.txt
       ↓
Docker build
       ↓
Docker image
       ↓
Container
       ↓
FastAPI
```

The key lesson is:

> **When GitHub Actions cannot build your Docker image, find the first failing Docker step and determine whether the problem is the Dockerfile, build context, dependencies, registry access, or CI environment before changing the application code.**
