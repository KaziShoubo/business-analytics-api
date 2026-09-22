from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.user import User
from fastapi import HTTPException
import jwt
import logging
from ..config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

password_hash = PasswordHash.recommended()


# Check the password
def verify_password(plain_password, hashed_password):
    check_password = password_hash.verify(plain_password, hashed_password)
    return check_password


# Find the user
def get_user_by_name(username, db: Session):
    res = select(User).where(User.username == username)
    result = db.execute(res)
    user = result.scalar_one_or_none()
    return user


# Authenticate the user by checking their username and password.
# Returns the user if the credentials are correct; otherwise raises a 401 error.
def authenticate_user(username, password, db: Session):
    user = get_user_by_name(username, db)
    if user is None:
        logger.warning(f"Failed login with user: {username}")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )


    check_password = verify_password(password, user.password_hash)

    if not check_password:
        logger.warning(f"Failed login with user: {username}")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )


    logger.info(f"User logged in successfully: {username}")

    return user


# Create a JWT access token containing user information and an expiration time.
# The token is signed using the configured secret key and algorithm.
def create_access_token(data: dict):
    to_encode = data.copy()  # should copy our data
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode["exp"] = expire

    access_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM

    )

    return access_token
