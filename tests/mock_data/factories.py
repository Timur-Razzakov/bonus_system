import factory
from factory.base import BaseFactory
from faker import Faker

from apps.core.models import Player, Level, Prize, LevelPrize, PlayerLevel
from apps.core.models.player import PlayerHistory

fake = Faker()


class PlayerFactory(BaseFactory):
    class Meta:
        model = Player

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name")


class LevelFactory(BaseFactory):
    class Meta:
        model = Level

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Faker("sentence", nb_words=2)
    order = factory.Faker("1", nb_words=2)


class PrizeFactory(BaseFactory):
    class Meta:
        model = Prize

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Faker("word")
    image = factory.Faker("image_url")
    description = factory.Faker("sentence")


class LevelPrizeFactory(BaseFactory):
    class Meta:
        model = LevelPrize

    id = factory.Sequence(lambda n: n + 1)
    level = factory.SubFactory(LevelFactory)
    level_id = factory.SelfAttribute("level.id")
    prize = factory.SubFactory(PrizeFactory)
    prize_id = factory.SelfAttribute("prize.id")
    is_primary = True


class PlayerLevelFactory(BaseFactory):
    class Meta:
        model = PlayerLevel

    id = factory.Sequence(lambda n: n + 1)
    player = factory.SubFactory(PlayerFactory)
    player_id = factory.SelfAttribute("player.id")
    level = factory.SubFactory(LevelFactory)
    level_id = factory.SelfAttribute("level.id")
    is_completed = False
    completed_at = None

    class Params:
        completed = factory.Trait(
            is_completed=True,
        )


class PlayerHistoryFactory(BaseFactory):
    class Meta:
        model = PlayerHistory

    id = factory.Sequence(lambda n: n + 1)
    player = factory.SubFactory(PlayerFactory)
    player_id = factory.SelfAttribute("player.id")
    level = factory.SubFactory(LevelFactory)
    level_id = factory.SelfAttribute("level.id")
    prize = factory.SubFactory(PrizeFactory)
    prize_id = factory.SelfAttribute("prize.id")
