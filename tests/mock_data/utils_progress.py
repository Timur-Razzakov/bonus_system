from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.core.models import Player, Level, Prize, LevelPrize, PlayerLevel  # проверь путь

async def make_player(session: AsyncSession, name: str = "Player") -> Player:
    p = Player(name=name)
    session.add(p)
    await session.flush()
    return p

async def make_level(session: AsyncSession, title: str, order: int) -> Level:
    l = Level(title=title, order=order)
    session.add(l)
    await session.flush()
    return l

async def make_prize(session: AsyncSession, title: str = "Prize", image: str = "img.png", description: str = "desc") -> Prize:
    pr = Prize(title=title, image=image, description=description)
    session.add(pr)
    await session.flush()
    return pr

async def link_level_prize(session: AsyncSession, level_id: int, prize_id: int, is_primary: bool = True) -> LevelPrize:
    lp = LevelPrize(level_id=level_id, prize_id=prize_id, is_primary=is_primary)
    session.add(lp)
    await session.flush()
    return lp

async def link_player_level(session: AsyncSession, player_id: int, level_id: int, is_completed: bool = False) -> PlayerLevel:
    pl = PlayerLevel(player_id=player_id, level_id=level_id, is_completed=is_completed)
    session.add(pl)
    await session.flush()
    return pl

async def get_player_level(session: AsyncSession, player_id: int, level_id: int) -> PlayerLevel | None:
    return await session.scalar(
        select(PlayerLevel).where(PlayerLevel.player_id == player_id, PlayerLevel.level_id == level_id)
    )
