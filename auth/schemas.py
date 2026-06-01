from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"

class LoginRequest(BaseModel):
    email:str
    password:str

class TokenPayload(BaseModel):
    name:str
    email:str
    password:str
