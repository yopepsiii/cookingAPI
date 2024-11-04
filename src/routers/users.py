import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds.users import crud_create_user, crud_get_user, crud_update_user, crud_delete_user
from src.db.db import get_db
from src.oauth import get_current_user
from src.schemas.auth import TokenData
from src.schemas.user import UserOut, UserOutFull, UserIn, UserPatch

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/{user_id}', response_model=UserOutFull, summary='Получить полную информацию о пользователе')
async def get_user(user_id: uuid.UUID,
                   db: AsyncSession = Depends(get_db)):
    return await crud_get_user(db, user_id)


@router.post("/", response_model=UserOutFull, status_code=201, summary='Создать нового пользователя')
async def create_user(new_data: UserIn,
                      db: AsyncSession = Depends(get_db),
                      ):
    return await crud_create_user(db, new_data)


@router.patch("/me", response_model=UserOutFull, summary='Обновить данные у пользователя')
async def update_user(updated_data: UserPatch,
                      current_user: TokenData = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    return await crud_update_user(db, uuid.UUID(current_user.user_id), updated_data)


@router.delete("/me", status_code=204, summary='Удалить свой аккаунт')
async def delete_user(current_user: TokenData = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    return await crud_delete_user(db, uuid.UUID(current_user.user_id))
