from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Prize(BaseModel):
    __tablename__ = "prizes"
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    image: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    level_prizes = relationship("LevelPrize", back_populates="prize")
    histories = relationship("PlayerHistory", back_populates="prize")
