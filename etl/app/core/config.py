from handlers.handlers import MovieLikeHandler, UserViewsHandler
from models.models import LikeEvent, ViewEvent

events_config = {
    "views": {
        "model": ViewEvent,
        "handlers": [UserViewsHandler]
    },
    "likes": {
        "model": LikeEvent,
        "handlers": [MovieLikeHandler]
    }
}
