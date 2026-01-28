from pydantic import BaseModel
from typing import Optional
from datetime import time


class TrainSearchResult(BaseModel):
    train_id: int
    train_number: str
    train_name: str
    source_departue: Optional[time]
    destination_arrival: Optional[time]


