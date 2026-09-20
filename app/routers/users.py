from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas.user import UserCreate, AdminUserCreate, UserResponse
from ..services.users_service import create_user, create_admin, get_users
from ..dependencies.auth_dependencies import get_current_admin
from ..models.user import User

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)):
    result = create_user(user_data, db)
    return result


# current_admin tells FastAPI to run get_current_admin()
# before executing the endpoint, restricting access to administrators.
@router.post("/admin", response_model=UserResponse)
def create_admin_endpoint(admin_data: AdminUserCreate, current_admin: User = Depends(get_current_admin),
                          db: Session = Depends(get_db)):
    result = create_admin(admin_data, db)
    return result


@router.get("/", response_model=list[UserResponse])
def get_users_endpoint(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    result = get_users(db)
    return result
