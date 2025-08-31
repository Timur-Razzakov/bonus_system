from datetime import datetime

from pydantic import BaseModel, Field


class AwardRequest(BaseModel):
    player_id: int = Field(ge=1)
    level_id: int = Field(ge=1)


class AwardResponse(BaseModel):
    player_id: int
    level_id: int
    prize_id: int | None = None
    prize_title: str | None = None
    awarded_at: datetime | None = None
