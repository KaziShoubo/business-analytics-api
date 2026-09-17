from fastapi import FastAPI
from .database.database import Base, engine

# Create all tables that are registered with Base
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Business Analytics API",
    description="A REST API for business sales management and analytics.",
    version="1.0.0",
)