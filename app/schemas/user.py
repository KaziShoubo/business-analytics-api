from pydantic import BaseModel


# data when coming into the API
class UserCreate(BaseModel):
    username: str
    password: str
    role: str


# Data when going out of the API
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
