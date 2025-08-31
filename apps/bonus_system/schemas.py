from datetime import datetime

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    player_id: int = Field(..., ge=1, description="ID игрока")
    level_id: int = Field(..., ge=1, description="ID уровня")


class AwardRequest(BaseSchema):
    pass


class AwardResponse(BaseSchema):
    prize_id: int | None = Field(None, description="ID приза")
    prize_title: str | None = Field(None, description="Название приза")
    awarded_at: datetime | None = Field(None, description="Дата награждения")


class PlayerHistoryOut(BaseSchema):
    id: int
    prize_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
