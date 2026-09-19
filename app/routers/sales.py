from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas.sale import SaleCreate, SaleResponse
from ..dependencies.auth_dependencies import get_current_user
from ..models.user import User
from ..services.sales_service import create_sale, get_sales, get_one_sale, update_sale, delete_sale

router = APIRouter()


@router.post("/", response_model=SaleResponse)
def create_sale_endpoint(sale: SaleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = create_sale(sale, current_user, db)
    return result


@router.get("/", response_model=list[SaleResponse])
def get_sales_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_sales(current_user, db)
    return result


@router.get("/{sale_id}", response_model=SaleResponse)
def get_one_sale_endpoint(sale_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_one_sale(sale_id, current_user, db)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="sale id not found"
        )

    return result


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale_endpoint(sale_id: int, sale_data: SaleCreate, current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    result = update_sale(sale_id, sale_data, current_user, db)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="sale id not found"
        )

    return result


@router.delete("/{sale_id}")
def delete_sale_endpoint(sale_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = delete_sale(sale_id, current_user, db)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="sale id not found"
        )

    return result
