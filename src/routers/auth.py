from typing import Annotated

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import models
from src.db.db import get_db
from src.oauth import generate_token
from src.schemas.auth import Token, TokenData
from src.utils import verify_password

router = APIRouter(tags=['Аутентификация'])


@router.post('/login', response_model=Token, summary='Войти в аккаунт')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    if not form_data.username and form_data.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Форма должна быть заполнена')

    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalars().first()

    if not user or not await verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверно введены почта или пароль')

    token = await generate_token(TokenData(email=form_data.username, user_id=str(user.id)))
    return {'access_token': token, 'type': 'bearer'}
