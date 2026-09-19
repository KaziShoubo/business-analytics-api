from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..dependencies.auth_dependencies import get_current_user
from ..models.user import User
from ..services.analytics_service import get_revenue, get_products, get_categories, get_summary

router = APIRouter()


@router.get("/revenue")
def get_revenue_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_revenue(current_user, db)
    return result


@router.get("/products")
def get_products_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_products(current_user, db)
    return result


@router.get("/categories")
def get_categories_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_categories(current_user, db)
    return result


@router.get("/summary")
def get_summary_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_summary(current_user, db)
    return result
