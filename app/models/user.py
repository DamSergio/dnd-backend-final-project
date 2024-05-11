from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class LoginUser(BaseModel):
    email: str
    password: str
