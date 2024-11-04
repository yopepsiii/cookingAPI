import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds.users import crud_get_user
from src.db import models
from src.schemas.score import ScoreIn, ScorePut


async def crud_get_scores(db: AsyncSession, limit: int = 50, page: int = 1, is_sort: bool = True) -> Sequence[models.Score]:
    offset = page * limit - limit

    res = await db.execute(select(models.Score).limit(limit).offset(offset))
    scores = res.scalars().all()

    if is_sort:
        scores = sorted(scores, key=lambda score: score.value + (score.created_at if score.updated_at is None else score.updated_at).timestamp(), reverse=True)

    return scores


async def crud_get_score(score_id: uuid.UUID, db: AsyncSession) -> models.Score | None:
    score = await db.get(models.Score, score_id)

    if not score:
        raise HTTPException(status_code=404, detail=f"Рекорд с ID {score_id} не найден.")

    return score


async def crud_create_score(new_data: ScoreIn, current_user_id: uuid.UUID, db: AsyncSession) -> models.Score | None:
    user = await crud_get_user(db, current_user_id)

    if user.best_score:
        raise HTTPException(status_code=409, detail=f'У пользователя уже существует лучший результат, измените его. ID результата: {user.best_score.id}')

    new_data_dict = new_data.dict()
    new_data_dict["user_id"] = current_user_id
    new_data_dict["created_at"] = datetime.now()

    new_score = models.Score(**new_data_dict)
    db.add(new_score)
    await db.commit()
    await db.refresh(new_score)

    return new_score


async def crud_update_score(score_id: uuid.UUID, updated_data: ScorePut,
                            current_user_id: uuid.UUID,
                            db: AsyncSession) -> models.Score | None:
    score = await crud_get_score(score_id, db)

    if score.user_id != current_user_id:
        raise HTTPException(status_code=403, detail=f'У вас нет доступа.')

    score.value = updated_data.value
    score.updated_at = datetime.now()

    await db.commit()
    await db.refresh(score)

    return score


async def crud_delete_score(score_id: uuid.UUID, current_user_id: uuid.UUID, db: AsyncSession):
    score = await crud_get_score(score_id, db)

    if score.user_id != current_user_id:
        raise HTTPException(status_code=403, detail=f'У вас нет доступа.')

    await db.delete(score)
    await db.commit()

    return True


