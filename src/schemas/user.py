import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    email: EmailStr
    password: constr(min_length=5)


class UserOut(UserBase):
    id: uuid.UUID


class UserOutFull(UserOut):
    email: EmailStr
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


class UserPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=5)] = None
