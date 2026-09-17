from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use SQLite and store the database in business_analytics.db
DATABASE_URL = "sqlite:///./business_analytics.db"

# The engine is essentially the connection/interface between our Python application and the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# creates database sessions when we need to interact with the database.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Creating a database Dependency
# It gives a database session that FastAPI can give to the endpoints
def get_db():
    db = SessionLocal()

    try:
        yield db  # Give the endpoint a database session, and when the request is finished, execute the cleanup code.
    finally:
        db.close()


Base = declarative_base()

# We are importing our models here because Base must exist before User and Sale can inherit from it
from ..models.user import User
from ..models.sale import Sale
