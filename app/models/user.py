"""
Our SQLAlchemy User model describes how data is stored in the database
"""

from ..database.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)