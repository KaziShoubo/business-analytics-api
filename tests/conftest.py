import pytest
from .test_database import test_engine, TestSessionLocal
from app.database.database import Base


"""
1. Create the test database tables before the test.
2. Provide a database session to the test.
3. Close the session afterward.
4. Clean up the tables after the test.
"""
@pytest.fixture
def db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=test_engine)
