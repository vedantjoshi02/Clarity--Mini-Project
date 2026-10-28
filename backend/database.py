from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Store the database inside the backend directory.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'clarity.db'}"

# Configure the SQLite database connection.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create a database session factory.
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
)


# Base class for all database models.
class Base(DeclarativeBase):
    pass


# Provide a database session to API endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()