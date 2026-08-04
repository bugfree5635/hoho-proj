# Python Package Import Path Failure

## Problem

Running pytest:

```bash
pytest
```

Error:

```
ModuleNotFoundError: No module named 'database'
```

Example:

```
app/main.py

from database.connection import engine
```

## Cause

The project structure:

```
hoho-proj

├── app
│   ├── database
│   │   └── connection.py
│   └── main.py
```

Python treats `app` as the package.

The import:

```python
from database.connection import engine
```

looks for:

```
root/database
```

but the actual location is:

```
root/app/database
```

## Solution

Use package relative import:

```python
from .database.connection import engine
```

or:

```python
from app.database.connection import engine
```

depending on execution method.

## Verify

Run from project root:

```bash
pytest
```

Expected:

```
collected X items

tests/test_api.py .....
```

## Lesson

Python imports depend on:

* current working directory
* package structure
* PYTHONPATH

Docker and local execution may require different import strategies.

