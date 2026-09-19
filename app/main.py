from fastapi import FastAPI
from .database.database import Base, engine
from .routers.sales import router as sales_router
from .routers.users import router as users_router
from .routers.auth import router as auth_router
from .routers.analytics import router as analytics_router

# Create all tables that are registered with Base
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Business Analytics API",
    description="A REST API for business sales management and analytics.",
    version="1.0.0",
)

app.include_router(
    sales_router,
    prefix="/api/v1/sales",
    tags=["Sales"]
)

app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["users"]
)


app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


app.include_router(
    analytics_router,
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)