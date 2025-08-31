import csv
import io

import pytest

from apps.bonus_system.services import iter_progress_csv
from tests.mock_data.factories import (
    PlayerFactory,
    LevelFactory,
    PrizeFactory,
    LevelPrizeFactory,
    PlayerLevelFactory,
    PlayerHistoryFactory,
)


@pytest.mark.asyncio
async def test_iter_progress_csv_streaming_and_delimiter(session):
    player = PlayerFactory()
    level1 = LevelFactory(order=1, title="start")
    level2 = LevelFactory(order=2, title="finish")
    prize = PrizeFactory(title="Icon +5")

    LevelPrizeFactory(level=level1, prize=prize, is_primary=True)
    PlayerLevelFactory(player=player, level=level1, is_completed=True)
    PlayerLevelFactory(player=player, level=level2, is_completed=True)
    PlayerHistoryFactory(player=player, level=level1, prize=prize)
    await session.flush()

    chunks = []
    async for chunk in iter_progress_csv(session):
        chunks.append(chunk)
    data = "".join(chunks)

    reader = csv.reader(io.StringIO(data), delimiter=";")
    rows = list(reader)

    assert rows[0] == ["player_id", "level_title", "is_completed", "prize_title"]

    assert rows[1][0] == str(player.id)
    assert rows[1][1] == "start"
    assert rows[1][2] in ("True", "true", "1")
    assert rows[1][3] == "Icon +5"

    assert rows[2][0] == str(player.id)
    assert rows[2][1] == "finish"
    assert rows[2][2] in ("True", "true", "1")
    assert rows[2][3] == ""  # на второй уровень приз не выдавался
