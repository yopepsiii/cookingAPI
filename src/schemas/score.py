import uuid
import datetime
from typing import Optional

from pydantic import BaseModel, confloat

from src.schemas.user import UserOut


class BaseScore(BaseModel):
    value: confloat(ge=0)


class ScoreIn(BaseScore):
    pass


class ScoreOut(BaseScore):
    id: uuid.UUID
    user: UserOut


class ScoreOutFull(ScoreOut):
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


class ScorePut(BaseScore):
    pass
