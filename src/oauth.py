from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from config import settings
from src.schemas.auth import TokenData
import jwt

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_password_bearer_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def generate_token(data: TokenData):
    data_dict = data.dict()
    to_encode = data_dict.copy()

    token_expire_in_minutes = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = token_expire_in_minutes
    token = jwt.encode(to_encode,
                       key=SECRET_KEY,
                       algorithm=ALGORITHM)

    return token


async def validate_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные данные пользователя.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(jwt=token,
                             key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        user_data = TokenData(**payload)
        return user_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ваша сессия была закончена, войдите снова")
    except jwt.DecodeError:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_password_bearer_scheme)):
    return await validate_token(token)
