from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class LevelPrize(BaseModel):
    __tablename__ = "level_prizes"
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"), index=True)
    prize_id: Mapped[int] = mapped_column(ForeignKey("prizes.id", ondelete="CASCADE"), index=True)
    # для того чтобы показывать, какой приз главный, если хотим иметь разные призы в каких-то случаях
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    level = relationship("Level", back_populates="level_prizes")
    prize = relationship("Prize")

    __table_args__ = (
        UniqueConstraint("level_id", "prize_id", name="uq_level_prize"),
        UniqueConstraint("level_id", "is_primary", name="uq_level_primary_once"),
    )


class Level(BaseModel):
    __tablename__ = "levels"
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    history = relationship("PlayerHistory", back_populates="level")
    level_prizes = relationship("LevelPrize", back_populates="level")
    player_levels = relationship("PlayerLevel", back_populates="level")

    __table_args__ = (Index("ix_levels_order", "order"),)
