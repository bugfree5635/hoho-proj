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