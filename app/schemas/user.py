from pydantic import BaseModel


# data when coming into the API
class UserCreate(BaseModel):
    username: str
    password: str
    # role: str     # I don't want a public registration request deciding its own privileges, let server decide this


class AdminUserCreate(BaseModel):
    username: str
    password: str


# Data when going out of the API
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
