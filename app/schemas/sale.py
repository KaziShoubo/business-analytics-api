"""
API needs to know: What data is the client allowed to send me?
#
Pydantic validates this incoming data before we put it into the database
"""

from pydantic import BaseModel
from datetime import date


class SaleCreate(BaseModel):
    product_name: str
    category: str
    quantity: int
    unit_price: float
    sale_date: date


class SaleResponse(BaseModel):
    id: int
    product_name: str
    category: str
    quantity: int
    unit_price: float
    sale_date: date
    user_id: int

