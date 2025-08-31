import datetime
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class BoostType(enum.Enum):
    SPEED = "speed"
    DOUBLE_POINTS = "double_points"


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_login = Column(DateTime)
    last_login = Column(DateTime)
    score = Column(Integer, default=0)

    boosts = relationship("PlayerBoost", back_populates="player")


class Boost(Base):
    __tablename__ = "boosts"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(BoostType), nullable=False)
    description = Column(String)


class PlayerBoost(Base):
    __tablename__ = "player_boosts"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    boost_id = Column(Integer, ForeignKey("boosts.id"))
    receipt_date = Column(DateTime, default=func.now())
    is_used = Column(Boolean, default=False)

    player = relationship("Player", back_populates="boosts")
    boost = relationship("Boost")


async def login(db: AsyncSession, player: Player):
    now = datetime.datetime.now()
    if not player.first_login:
        player.first_login = now
    if not player.last_login or (now.date() != player.last_login.date()):
        player.score += 10
    player.last_login = now
    db.add(player)
    await db.commit()
    await db.refresh(player)
