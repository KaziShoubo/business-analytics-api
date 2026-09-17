from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from pwdlib import PasswordHash

router = APIRouter()

password_hash = PasswordHash.recommended()


@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    real_password = user_data.password
    hashed_password = password_hash.hash(real_password)

    user = User(
        username=user_data.username,
        password_hash=hashed_password,
        role=user_data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
