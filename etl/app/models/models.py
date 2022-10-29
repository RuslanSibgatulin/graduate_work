from pydantic import BaseModel, Field, root_validator


class EventMixin(BaseModel):
    user_id: str
    movie_id: str
    event_time: int


class ViewEvent(EventMixin):
    time: int
    total_time: int
    percent: float

    @root_validator(pre=True)
    def fill_percent(cls, values):
        if "percent" not in values:
            pos, total = values.get("time", 0), values.get("total_time", 0)
            values["percent"] = pos / total * 100
        return values


class LikeEvent(EventMixin):
    score: int = Field(ge=1, le=10)
