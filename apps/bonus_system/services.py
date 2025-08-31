from __future__ import annotations

import csv
from datetime import UTC, datetime
import io

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from apps.core.exceptions.message_exception import MessageException
from apps.core.models import Level, LevelPrize, Player, PlayerLevel, Prize
from apps.core.models.player import PlayerHistory


async def level_is_passed(
    session: AsyncSession,
    *,
    player_id: int,
    level_id: int,
) -> PlayerHistory:
    now = datetime.now(UTC)

    player_level = await session.scalar(
        select(PlayerLevel)
        .where(
            PlayerLevel.player_id == player_id,
            PlayerLevel.level_id == level_id,
        )
        .with_for_update()
    )
    if player_level is None:
        player_level = PlayerLevel(
            player_id=player_id,
            level_id=level_id,
            is_completed=True,
            completed_at=now,
        )
        session.add(player_level)
        await session.flush()
    elif not player_level.is_completed:
        player_level.is_completed = True
        player_level.completed_at = now

    history = await session.scalar(
        select(PlayerHistory).where(
            PlayerHistory.player_id == player_id,
            PlayerHistory.level_id == level_id,
        )
    )
    if history:
        return history

    level_prize = await session.scalar(
        select(LevelPrize)
        .options(joinedload(LevelPrize.prize))
        .where(LevelPrize.level_id == level_id)
        .order_by(LevelPrize.is_primary.desc())
        .limit(1)
    )
    if level_prize is None:
        raise MessageException(status_code=404, message_id="Для уровня не настроен приз")

    history = PlayerHistory(
        player_id=player_id,
        level_id=level_id,
        prize_id=level_prize.prize_id,
    )
    session.add(history)

    try:
        await session.flush()
    except IntegrityError:
        existing = await session.scalar(
            select(PlayerHistory).where(
                PlayerHistory.player_id == player_id,
                PlayerHistory.level_id == level_id,
            )
        )
        if existing:
            return existing
        raise
    await session.commit()
    return history


def build_progress_select():
    return (
        select(
            Player.id.label("player_id"),
            Level.title.label("level_title"),
            PlayerLevel.is_completed.label("is_completed"),
            Prize.title.label("prize_title"),
        )
        .join(PlayerLevel, PlayerLevel.player_id == Player.id)
        .join(Level, Level.id == PlayerLevel.level_id)
        .outerjoin(
            PlayerHistory,
            and_(PlayerHistory.player_id == Player.id, PlayerHistory.level_id == Level.id),
        )
        .outerjoin(Prize, Prize.id == PlayerHistory.prize_id)
        .order_by(Player.id, Level.order)
    )


async def iter_progress_csv(session: AsyncSession):
    head_buf = io.StringIO()
    w = csv.writer(head_buf)
    w.writerow(["player_id", "level_title", "is_completed", "prize_title"])
    yield head_buf.getvalue()
    head_buf.close()

    stmt = build_progress_select()
    result = await session.stream(stmt)

    async for row in result:
        row_buf = io.StringIO()
        writer = csv.writer(row_buf)
        writer.writerow([
            row.player_id,
            row.level_title,
            bool(row.is_completed),
            row.prize_title or "",
        ])
        yield row_buf.getvalue()
        row_buf.close()


async def export_progress_to_csv(session: AsyncSession, file_path: str) -> str:
    async_gen = iter_progress_csv(session)
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        async for chunk in async_gen:
            f.write(chunk)
    return file_path
