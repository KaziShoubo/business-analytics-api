from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas.user import UserCreate, UserResponse
from ..services.users_service import create_user, get_users

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)):
    result = create_user(user_data, db)
    return result


@router.get("/", response_model=list[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)):
    result = get_users(db)
    return result
