from handlers.handlers import UserViewsHandler, MovieLikeHandler
from models.models import ViewEvent, LikeEvent

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
