from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from ..database.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    sale_date = Column(Date)
    user_id = Column(Integer, ForeignKey(
        "users.id"))  # Store a user's ID here, and that ID must reference a user in the users table
