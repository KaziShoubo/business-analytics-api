from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, AdminUserCreate
from pwdlib import PasswordHash
from sqlalchemy import select

password_hash = PasswordHash.recommended()


# assigning role="user" will automatically assign all user's role as user, we still need to define admin role
def create_user(user_data: UserCreate, db: Session):
    real_password = user_data.password
    hashed_password = password_hash.hash(real_password)

    user = User(
        username=user_data.username,
        password_hash=hashed_password,
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# it creates the admin by following the AdminUserCreate schema
def create_admin(user_data: AdminUserCreate, db: Session):
    real_password = user_data.password
    hashed_password = password_hash.hash(real_password)

    admin_user = User(
        username=user_data.username,
        password_hash=hashed_password,
        role="admin"
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return admin_user


def get_users(db: Session):
    res = select(User)
    result = db.execute(res)
    users = result.scalars().all()

    return users
