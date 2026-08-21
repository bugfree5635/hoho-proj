import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, Response
from prometheus_client import generate_latest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .api.auth import router as auth_router
from .api.employees import router
from .database.connection import engine, get_database
from .monitoring.metrics import REQUEST_COUNT, REQUEST_TIME


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # shutdown
    engine.dispose()


app = FastAPI(
    title="Employee Management API",
    description="""
A REST API for managing employees and users.

## Features

- Employee management
- User authentication
- JWT authentication
- PostgreSQL database
- Health monitoring
""",
    version="1.0",
    contact={
        "name": "Henry",
    },
    lifespan=lifespan,
)


app.include_router(router)
app.include_router(auth_router)


@app.get("/health")
def health_check(db: Session = Depends(get_database)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "unavailable"},
        )


@app.middleware("http")
async def metrics_middleware(request, call_next):

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()

    REQUEST_TIME.labels(endpoint=request.url.path).observe(duration)

    return response


@app.get("/metrics")
def metrics():

    return Response(generate_latest(), media_type="text/plain")
