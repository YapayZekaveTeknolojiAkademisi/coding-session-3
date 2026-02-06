from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str

class RegisterResponse(BaseModel):
    id: str
    email: str
    message: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id: str
    email: str
    access_token: str
    refresh_token: str
    message: str

class LogoutRequest(BaseModel):
    token: str

class LogoutResponse(BaseModel):
    message: str

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    message: str
