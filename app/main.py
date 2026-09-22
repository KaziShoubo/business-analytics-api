from fastapi import FastAPI
import time
from .database.database import Base, engine
from .routers.sales import router as sales_router
from .routers.users import router as users_router
from .routers.auth import router as auth_router
from .routers.analytics import router as analytics_router
import logging
from . import logging_config


logger = logging.getLogger(__name__)

# Create all tables that are registered with Base
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Business Analytics API",
    description="A REST API for business sales management and analytics.",
    version="1.0.0",
)
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    logger.info(
        f"HTTP {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.4f}s"
    )

    return response


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