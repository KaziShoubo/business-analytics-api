from sqlalchemy.orm import Session
from ..models.user import User
from ..models.sale import Sale
from sqlalchemy import select, func
import logging

logger = logging.getLogger(__name__)


# return total revenue per user. revenue = quantity*unit_price
def get_revenue(current_user: User, db: Session):
    query = select(Sale).where(Sale.user_id == current_user.id)
    result = db.execute(query)
    sales = result.scalars().all()

    sales_revenue = 0
    for i in sales:
        total = i.quantity * i.unit_price
        sales_revenue += total

    logger.info(
        f"Revenue analytics requested | User: {current_user.username}"
    )
    return {"total_revenue": sales_revenue}


# return every product with their quantity soled and revenue from them
def get_products(current_user: User, db: Session):
    query = select(
        Sale.product_name,
        func.sum(Sale.quantity),
        func.sum(Sale.quantity * Sale.unit_price)
    ).where(
        Sale.user_id == current_user.id
    ).group_by(
        Sale.product_name
    )
    res = db.execute(query)

    # The query returns multiple selected columns, not complete Sale objects.
    # scalars() would keep only the first column, so we use all() and convert
    # each SQLAlchemy Row into a dictionary that FastAPI can return as JSON.
    result = res.all()

    products = []
    for row in result:
        row_dict = {
            "product_name": row[0],
            "quantity_sold": row[1],
            "revenue": row[2]
        }

        products.append(row_dict)

    logger.info(
        f"Products analytics requested | User: {current_user.username}"
    )

    return products


# Return every category with its quantity sold and revenue.
def get_categories(current_user: User, db: Session):
    query = select(
        Sale.category,
        func.sum(Sale.quantity),
        func.sum(Sale.quantity * Sale.unit_price)
    ).where(
        Sale.user_id == current_user.id
    ).group_by(
        Sale.category
    )
    res = db.execute(query)
    result = res.all()

    categories = []
    for row in result:
        row_dict = {
            "category": row[0],
            "quantity_sold": row[1],
            "revenue": row[2]
        }

        categories.append(row_dict)

    logger.info(
        f"Categories analytics requested | User: {current_user.username}"
    )

    return categories


# Gives a summary of our analysis
def get_summary(current_user: User, db: Session):
    res = select(Sale).where(Sale.user_id == current_user.id)
    result = db.execute(res)
    sales = result.scalars().all()

    total_revenue = 0
    for i in sales:
        total = i.quantity * i.unit_price
        total_revenue += total

    total_orders = len(sales)

    if total_orders > 0:
        average_order_value = total_revenue / total_orders
    else:
        average_order_value = 0

    logger.info(
        f"Summary analytics requested | User: {current_user.username}"
    )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": average_order_value
    }



