from contextlib import asynccontextmanager
from clients import router as clients_router
from fastapi import FastAPI
from products import router as products_router
from sqlalchemy import text
from goals import router as goals_router
import models
from auth import router as auth_router
from database import Base, engine
from simulations import router as simulations_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables for the imported SQLAlchemy models.
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Clarity API",
    description=(
        "Investment decision-support and "
        "financial scenario simulation API."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Register authentication endpoints.
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(products_router)
app.include_router(goals_router)
app.include_router(simulations_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to the Clarity API!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }