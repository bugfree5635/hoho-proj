Yes. Let's reorganize the FastAPI application according to your architecture.

Final structure:

```text
employee-api/

├── app/
│
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│
│   ├── config/
│   │   └── settings.py
│
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│
│   ├── api/
│   │   └── employees.py
│
│   ├── schemas/
│   │   └── employee.py
│
│   └── tests/
│       └── test_api.py
```

---

# app/main.py

Application entry point.

```python
from fastapi import FastAPI

from database.connection import engine
from database.models import Base

from api.employees import router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    version="1.0"
)


app.include_router(router)


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }
```

---

# app/requirements.txt

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic-settings
pytest
httpx
```

---

# app/.env.example

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=company
DATABASE_USER=admin
DATABASE_PASSWORD=password
```

---

# app/config/settings.py

Configuration management.

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_HOST: str

    DATABASE_PORT: int

    DATABASE_NAME: str

    DATABASE_USER: str

    DATABASE_PASSWORD: str


    class Config:
        env_file = ".env"



settings = Settings()
```

---

# app/database/connection.py

Database connection.

```python
from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

from config.settings import settings



DATABASE_URL = (
    f"postgresql://"
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)



engine = create_engine(
    DATABASE_URL
)



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)



Base = declarative_base()



def get_database():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
```

---

# app/database/models.py

Database tables.

```python
from sqlalchemy import (
    Column,
    Integer,
    String
)


from database.connection import Base



class Employee(Base):

    __tablename__ = "employees"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    email = Column(
        String,
        unique=True,
        nullable=False
    )


    department = Column(
        String,
        nullable=False
    )
```

---

# app/schemas/employee.py

API request/response format.

```python
from pydantic import BaseModel



class EmployeeCreate(BaseModel):

    name: str

    email: str

    department: str



class EmployeeResponse(BaseModel):

    id: int

    name: str

    email: str

    department: str



    class Config:

        from_attributes = True
```

---

# app/api/employees.py

REST API routes.

```python
from fastapi import (
    APIRouter,
    Depends
)


from sqlalchemy.orm import Session


from database.connection import get_database

from database.models import Employee

from schemas.employee import (
    EmployeeCreate,
    EmployeeResponse
)



router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)



@router.get(
    "/",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_database)
):

    return db.query(Employee).all()



@router.post(
    "/",
    response_model=EmployeeResponse
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_database)
):

    new_employee = Employee(

        name=employee.name,

        email=employee.email,

        department=employee.department
    )


    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)


    return new_employee
```

---

# app/tests/test_api.py

API testing.

```python
from fastapi.testclient import TestClient

from main import app



client = TestClient(app)



def test_health():

    response = client.get(
        "/health"
    )


    assert response.status_code == 200


    assert response.json() == {
        "status":"ok"
    }
```

---

# app/Dockerfile

```dockerfile
FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install \
    --no-cache-dir \
    -r requirements.txt



COPY . .



CMD [
"uvicorn",
"main:app",
"--host",
"0.0.0.0",
"--port",
"8000"
]
```

---

# Run locally

Inside `app/`:

Create environment:

```bash
cp .env.example .env
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn main:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

# Why this architecture is better for Sysadmin/DevOps

This structure demonstrates real separation:

```
main.py
   |
   |
api/
   |
business API

schemas/
   |
data format

database/
   |
storage layer

config/
   |
environment management

tests/
   |
quality check
```

This is closer to a production project than putting everything into one `main.py`.

For your infrastructure portfolio, this app can later connect to:

```
Nginx
 |
Docker
 |
FastAPI
 |
PostgreSQL
 |
Prometheus
 |
Grafana
 |
Ansible deployment
```

which matches your Sysadmin → DevOps roadmap.
