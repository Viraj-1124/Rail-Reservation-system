from pydantic import BaseModel
from datetime import time


class TrainSearchResult(BaseModel):
    train_id: int
    train_number: str
    train_name: str
    source_departue: time
    destination_arrival: time


