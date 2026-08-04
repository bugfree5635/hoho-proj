# GitHub Actions Pipeline

## Purpose

GitHub Actions provides automated execution after code changes.

This project uses it for CI/CD.


## Workflow Location

```

.github/

└── workflows/
└── ci.yml

```

## Pipeline Flow

```

Push code

|

GitHub Actions Trigger

|

Install Python

|

Install dependencies

|

Run pytest

|

Build Docker image

|

Success

```


## Runner

Current runner:

```

ubuntu-latest

```


Reason:

GitHub provides free Ubuntu runners.

The runner is temporary and destroyed after workflow completion.


## Why not Ubuntu 26.04?

GitHub does not currently provide every Ubuntu version.

For CI:

```

ubuntu-latest

```

is recommended because:

- maintained by GitHub
- security updates included
- stable environment


## Failure Handling

If tests fail:

```

Code Push

|

CI

|

pytest failed

|

Merge blocked

```


This prevents broken code entering main branch.


## Future CD

Add:

```

Build image

|

Push Docker Hub

|

SSH into server

|

Deploy compose stack

```
