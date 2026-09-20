"""
Authentication dependencies for the API.

This file handles:
1. Extracting the JWT Bearer token from incoming requests.
2. Decoding and validating the JWT.
3. Getting the username from the token.
4. Finding the corresponding user in the database.
5. Returning the authenticated user.
6. Raising a 401 error when authentication fails.
"""

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import jwt
from ..config import SECRET_KEY, ALGORITHM
from ..database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login"
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    username = payload["sub"]

    query = select(User).where(User.username == username)
    result = db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    return user


def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user
