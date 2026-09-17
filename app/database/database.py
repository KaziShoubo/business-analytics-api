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

Base = declarative_base()

# We are importing our models here because Base must exist before User and Sale can inherit from it
from ..models.user import User
from ..models.sale import Sale