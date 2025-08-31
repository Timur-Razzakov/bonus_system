from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Player(BaseModel):
    __tablename__ = "players"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    player_levels = relationship("PlayerLevel", back_populates="player", cascade="all, delete-orphan")
    history = relationship("PlayerHistory", back_populates="player", cascade="all, delete-orphan")


class PlayerLevel(BaseModel):
    __tablename__ = "player_levels"
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"), index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    player = relationship("Player", back_populates="player_levels")
    level = relationship("Level", back_populates="player_levels")

    __table_args__ = (
        UniqueConstraint("player_id", "level_id", name="uq_player_level"),
        Index("ix_player_level", "player_id", "level_id"),
    )


class PlayerHistory(BaseModel):
    __tablename__ = "player_history"
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"), index=True)
    prize_id: Mapped[int] = mapped_column(ForeignKey("prizes.id", ondelete="CASCADE"), nullable=False)

    player = relationship("Player", back_populates="history")
    prize = relationship("Prize")

    __table_args__ = (
        UniqueConstraint("player_id", "level_id", name="uq_history_player_level"),
        Index("ix_history_player_level", "player_id", "level_id"),
    )
