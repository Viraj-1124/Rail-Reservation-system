from pydantic import BaseModel
from datetime import time

class RouteCreate(BaseModel):
    train_number : int
    station_code : int
    arrival_time: time | None
    departure_time: time | None
    day_number: int
    sequence: int