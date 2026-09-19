from sqlalchemy.orm import Session
from ..models.sale import Sale
from ..schemas.sale import SaleCreate
from sqlalchemy import select
from ..models.user import User


def create_sale(sale: SaleCreate, current_user: User, db: Session):
    new_sale = Sale(
        product_name=sale.product_name,
        category=sale.category,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        sale_date=sale.sale_date,
        user_id=current_user.id
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale


# Sales belonging to the currently authenticated use
def get_sales(current_user: User, db: Session):
    res = select(Sale).where(Sale.user_id == current_user.id)
    result = db.execute(res)
    sales = result.scalars().all()

    return sales


def get_one_sale(sale_id: int, current_user: User, db: Session):
    res = select(Sale).where(Sale.id == sale_id, Sale.user_id == current_user.id)
    result = db.execute(res)
    sale = result.scalar_one_or_none()

    if sale is None:
        return None

    return sale


def update_sale(sale_id: int, sale_data: SaleCreate, current_user: User, db: Session):
    res = select(Sale).where(Sale.id == sale_id, Sale.user_id == current_user.id)
    result = db.execute(res)
    sale = result.scalar_one_or_none()

    if sale is None:
        return None

    sale.product_name = sale_data.product_name
    sale.category = sale_data.category
    sale.quantity = sale_data.quantity
    sale.unit_price = sale_data.unit_price
    sale.sale_date = sale_data.sale_date

    db.commit()
    db.refresh(sale)

    return sale


def delete_sale(sale_id: int, current_user: User, db: Session):
    res = select(Sale).where(Sale.id == sale_id, Sale.user_id == current_user.id)
    result = db.execute(res)
    sale = result.scalar_one_or_none()

    if sale is None:
        return None

    db.delete(sale)
    db.commit()

    return {"message": "Sale deleted successfully"}
