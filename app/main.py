import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest

from .api.auth import router as auth_router
from .api.employees import router
from .database.connection import engine
from .monitoring.metrics import REQUEST_COUNT, REQUEST_TIME


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # shutdown
    engine.dispose()


app = FastAPI(title="Employee Management API", version="1.0", lifespan=lifespan)


app.include_router(router)
app.include_router(auth_router)


@app.get("/health")
def health_check():

    return {"status": "ok"}


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
