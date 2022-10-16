from handlers.handlers import UserViewsHandler
from models.models import ViewEvent

events_config = {
    "views": {
        "model": ViewEvent,
        "handlers": [UserViewsHandler]
    },
}
