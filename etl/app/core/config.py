from handlers.handlers import MovieLikeHandler, UserViewsHandler
from models.models import LikeEvent, ViewEvent

events_config = {
    "views": {
        "model": ViewEvent,
        "handlers": [UserViewsHandler]
    },
    "like": {
        "model": LikeEvent,
        "handlers": [MovieLikeHandler]
    }
}
