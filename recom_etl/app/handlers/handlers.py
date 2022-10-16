import logging
from models.models import ViewEvent

logger = logging.getLogger(__name__)


class UserViewsHandler():
    def __init__(self, event: str):
        super().__init__()
        self.event = event

    async def __call__(self, context: ViewEvent) -> None:
        if 80 < context.percent < 85:
            logger.info(
                "Movie %s user %s progress %s on event <%s>",
                context.movie_id,
                context.user_id,
                context.percent,
                self.event
            )
            await self.add_user_view(context.user_id, context.movie_id)
