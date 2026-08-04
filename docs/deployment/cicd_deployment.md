# CI/CD Deployment

## Overview

This project uses GitHub Actions to automate:

- Python testing
- Dependency installation
- Docker image building
- Deployment preparation


Workflow:

```

Developer

|
|
git push

|
|
GitHub Actions

|
|
Run tests

|
|
Build Docker image

|
|
Deploy application

```


## CI Pipeline

Continuous Integration checks that new code does not break the application.

Current CI tasks:

1. Checkout source code

2. Setup Python environment

3. Install dependencies

4. Run pytest


Example:

```yaml
name: CI

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main


jobs:

  test:

    runs-on: ubuntu-latest

    steps:

      - name: Checkout code
        uses: actions/checkout@v4


      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"


      - name: Install dependencies
        run:

          pip install -r app/requirements.txt


      - name: Run tests
        run:

          pytest
```

## Environment Variables

GitHub Actions runs on a clean machine.

It does not contain:

* local .env
* database configuration
* Docker network

CI variables should be configured:

```
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

Example:

```yaml
env:

  DATABASE_HOST: localhost

  DATABASE_PORT: 5432

  DATABASE_NAME: company

  DATABASE_USER: admin

  DATABASE_PASSWORD: password
```

## Docker Build Pipeline

After tests pass:

```
pytest

   |

docker build

   |

Docker image

```

Example:

```yaml
- name: Build Docker image

  run:

    docker build \
    -t employee-api \
    ./app
```

## Deployment Pipeline

Future deployment:

```
GitHub Actions

        |

        |

SSH

        |

        |

Ubuntu Server

        |

        |

Docker Compose

        |

        |

Application running

```

Deployment steps:

1. Connect server using SSH key

2. Pull latest code

3. Rebuild containers

4. Restart services

Example:

```bash
docker compose pull

docker compose up -d --build
```

## Secrets Management

Sensitive data should not be stored in Git.

Example:

Bad:

```
DATABASE_PASSWORD=password
```

Good:

```
GitHub Secrets

        |

        |

Workflow Environment

        |

        |

Application
```

## Current Status

Implemented:

* GitHub Actions CI
* Automated pytest
* Docker build verification

Future improvements:

* Docker image push to registry
* Automatic deployment
* HTTPS deployment
* Rollback strategy
