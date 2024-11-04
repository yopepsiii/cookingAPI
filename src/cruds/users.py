import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import utils
from src.db import models
from src.schemas.user import UserIn, UserPatch
from src.utils import hash_password


async def crud_get_user(db: AsyncSession, user_id: uuid.UUID):
    user = await db.get(models.User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} не найден.")

    return user


async def crud_create_user(db: AsyncSession, new_data: UserIn):
    db_user = await db.execute(select(models.User).where(models.User.email == new_data.email))
    user = db_user.scalars().one_or_none()

    if user:
        raise HTTPException(status_code=409, detail=f"Пользователь с такой почтой уже существует.")

    new_data_dict = new_data.dict()
    new_data_dict['created_at'] = datetime.now()
    new_data_dict['password'] = await hash_password(new_data_dict['password'])

    new_user = models.User(**new_data_dict)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def crud_update_user(db: AsyncSession, current_user_id: uuid.UUID, new_data: UserPatch):
    new_values = new_data.dict(exclude_unset=True)

    if not new_values:
        return

    if new_values.get('password'):
        new_values['password'] = await utils.hash_password(new_data.password)

    current_user = await crud_get_user(db, current_user_id)

    for key, value in new_values.items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user


async def crud_delete_user(db: AsyncSession, current_user_id: uuid.UUID):
    current_user = await crud_get_user(db, current_user_id)

    await db.delete(current_user)
    await db.commit()

    return True
