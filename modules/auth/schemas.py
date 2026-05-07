from pydantic import BaseModel


class LoginPayload(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    access_token: str
    message: str


