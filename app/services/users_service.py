from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from pwdlib import PasswordHash
from sqlalchemy import select


password_hash = PasswordHash.recommended()


def create_user(user_data: UserCreate, db: Session):
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


def get_users(db: Session):
    res = select(User)
    result = db.execute(res)
    users = result.scalars().all()

    return users
