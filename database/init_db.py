from database.connection import Base, engine

# Import models so SQLAlchemy registers all tables
from database import models


def initialize_database():

    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()
