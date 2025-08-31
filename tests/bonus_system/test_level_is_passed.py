import pytest
from sqlalchemy import select, func

from apps.bonus_system import services  # там лежит level_is_passed
from apps.core.models import PlayerLevel
from apps.core.models.player import PlayerHistory
from tests.mock_data.factories  import (
    PlayerFactory,
    LevelFactory,
    PrizeFactory,
    LevelPrizeFactory,
    PlayerLevelFactory,
)


@pytest.mark.asyncio
async def test_award_creates_player_level_and_history(session):
    player = PlayerFactory()
    level = LevelFactory(order=1)
    prize = PrizeFactory()

    LevelPrizeFactory(level=level, prize=prize, is_primary=True)
    await session.flush()

    history = await services.level_is_passed(
        session=session, player_id=player.id, level_id=level.id
    )

    assert history.player_id == player.id
    assert history.level_id == level.id
    assert history.prize_id == prize.id

    pl = await session.scalar(
        select(PlayerLevel).where(
            PlayerLevel.player_id == player.id,
            PlayerLevel.level_id == level.id,
        )
    )
    assert pl is not None
    assert pl.is_completed is True
    assert pl.completed_at is not None

    history2 = await services.level_is_passed(
        session=session, player_id=player.id, level_id=level.id
    )
    assert history2.id == history.id

    count = await session.scalar(
        select(func.count()).select_from(PlayerHistory).where(
            PlayerHistory.player_id == player.id,
            PlayerHistory.level_id == level.id,
        )
    )
    assert count == 1


@pytest.mark.asyncio
async def test_award_updates_existing_player_level(session):
    player = PlayerFactory()
    level = LevelFactory(order=1)
    prize = PrizeFactory()
    LevelPrizeFactory(level=level, prize=prize, is_primary=True)

    PlayerLevelFactory(player=player, level=level, is_completed=False, completed_at=None)
    await session.flush()

    await services.level_is_passed(session=session, player_id=player.id, level_id=level.id)

    pl = await session.scalar(
        select(PlayerLevel).where(
            PlayerLevel.player_id == player.id,
            PlayerLevel.level_id == level.id,
        )
    )
    assert pl.is_completed is True
    assert pl.completed_at is not None

    ph = await session.scalar(
        select(PlayerHistory).where(
            PlayerHistory.player_id == player.id,
            PlayerHistory.level_id == level.id,
        )
    )
    assert ph is not None
    assert ph.prize_id == prize.id


@pytest.mark.asyncio
async def test_award_picks_primary_prize(session):
    player = PlayerFactory()
    level = LevelFactory(order=1)
    non_primary = PrizeFactory()
    primary = PrizeFactory()

    LevelPrizeFactory(level=level, prize=non_primary, is_primary=False)
    LevelPrizeFactory(level=level, prize=primary, is_primary=True)
    await session.flush()

    history = await services.level_is_passed(
        session=session, player_id=player.id, level_id=level.id
    )
    assert history.prize_id == primary.id


@pytest.mark.asyncio
async def test_award_raises_without_configured_prize(session):
    player = PlayerFactory()
    level = LevelFactory(order=1)
    await session.flush()

    with pytest.raises(Exception):
        await services.level_is_passed(
            session=session, player_id=player.id, level_id=level.id
        )
