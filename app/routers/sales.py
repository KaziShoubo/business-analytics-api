from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.sale import Sale
from ..schemas.sale import SaleCreate, SaleResponse


router = APIRouter()


@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    new_sale = Sale(
        product_name=sale.product_name,
        category=sale.category,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        sale_date=sale.sale_date,
        user_id=1
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

