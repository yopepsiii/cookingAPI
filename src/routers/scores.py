import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds.scores import crud_get_scores, crud_get_score, crud_create_score, crud_update_score, crud_delete_score
from src.db.db import get_db
from src.oauth import get_current_user
from src.schemas.auth import TokenData
from src.schemas.score import ScoreOut, ScoreOutFull, ScoreIn, ScorePut

router = APIRouter(prefix='/scores', tags=['Рекорды'])


@router.get("/", response_model=list[ScoreOut], summary='Получить топ всех рекордов')
async def get_scores(db: AsyncSession = Depends(get_db), limit: int = 50, page: int = 1, is_sorted: bool = True):
    return await crud_get_scores(db, limit, page, is_sort=is_sorted)


@router.get('/{score_id}', response_model=ScoreOutFull, summary='Получить полную информацию о рекорде')
async def get_score(score_id: uuid.UUID,
                    db: AsyncSession = Depends(get_db)):
    return await crud_get_score(score_id, db)


@router.post("/",
             response_model=ScoreOutFull,
             status_code=201,
             summary='Создать новый рекорд')
async def create_score(score_data: ScoreIn,
                       db: AsyncSession = Depends(get_db),
                       current_user: TokenData = Depends(get_current_user)):
    return await crud_create_score(score_data, uuid.UUID(current_user.user_id), db)


@router.put("/{score_id}", response_model=ScoreOutFull, summary='Изменить данные о рекорде')
async def update_score(score_id: uuid.UUID,
                       updated_score_data: ScorePut,
                       db: AsyncSession = Depends(get_db),
                       current_user: TokenData = Depends(get_current_user)):
    return await crud_update_score(score_id, updated_score_data, uuid.UUID(current_user.user_id), db)


@router.delete('/{score_id}', status_code=204, summary='Удалить рекорд')
async def delete_score(score_id: uuid.UUID,
                       db: AsyncSession = Depends(get_db),
                       current_user: TokenData = Depends(get_current_user)):
    return await crud_delete_score(score_id, uuid.UUID(current_user.user_id), db)
