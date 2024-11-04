from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email: EmailStr
    user_id: str


class Token(BaseModel):
    access_token: str
    type: str
