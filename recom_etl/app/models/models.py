from pydantic import BaseModel, root_validator


class ViewEvent(BaseModel):
    user_id: str
    movie_id: str
    time: int
    total_time: int
    percent: float
    event_time: int

    @root_validator(pre=True)
    def fill_percent(cls, values):
        if "percent" not in values:
            pos, total = values.get("time", 0), values.get("total_time", 0)
            values["percent"] = pos / total * 100
        return values
