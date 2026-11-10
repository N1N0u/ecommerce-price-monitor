from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.settings import DATABASE_URL


# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False
)


# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Base class for database models
class Base(DeclarativeBase):
    pass


# Database session generator
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
