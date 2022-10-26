import logging
from typing import Any

from core.settings import mongo_settings
from db.mongo import MongoInterface
from models.models import LikeEvent, ViewEvent

logger = logging.getLogger(__name__)


class BaseHandlerMongo(MongoInterface):
    def __init__(self, event: str) -> None:
        super().__init__(
            mongo_settings.mongo_uri, mongo_settings.MONGO_DB
        )
        self.event = event

    async def load(self, context: Any) -> Any:
        pass


class UserViewsHandler(BaseHandlerMongo):
    def __init__(self, event: str) -> None:
        super().__init__(event)

    async def load(self, context: ViewEvent) -> None:
        """Save movie as viewed only if progress percent larger than 80%
        Args:
            context (ViewEvent): Event data
        """
        div, mod = divmod(context.percent, 10)
        if mod == 0 and div > 8:
            logger.info(
                "Movie %s viewed by user %s: progress %s on event <%s>",
                context.movie_id,
                context.user_id,
                context.percent,
                self.event
            )
            await self.add_view_to_profile(
                context.user_id,
                context.movie_id,
                context.event_time
            )


class MovieLikeHandler(BaseHandlerMongo):
    def __init__(self, event: str) -> None:
        super().__init__(event)

    async def load(self, context: LikeEvent) -> None:
        logger.info(
            "Movie %s is rated at %s by user %ss",
            context.movie_id,
            context.score,
            context.user_id,
        )
        await self.add_like_to_profile(
            context.user_id,
            context.movie_id,
            context.score
        )
