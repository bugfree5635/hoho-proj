from fastapi import FastAPI

from database.connection import engine
from database.models import Base

from api.employees import router

import time

from prometheus_client import generate_latest
from fastapi.responses import Response

from monitoring.metrics import (
    REQUEST_COUNT,
    REQUEST_TIME
)

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

@app.middleware("http")
async def metrics_middleware(request, call_next):

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time


    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()


    REQUEST_TIME.labels(
        endpoint=request.url.path
    ).observe(duration)


    return response

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )
