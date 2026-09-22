# How could we make the application use a different database when running tests,
# without changing the production/development database URL
# use- dependency_overrides

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///./business_analytics_test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()