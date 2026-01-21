from pydantic import BaseModel
from datetime import date

class TrainScheduleCreate(BaseModel):
    train_number : str
    journey_date: date
    status: str = "ACTIVE"


class TrainScheduleResponse(BaseModel):
    id: int
    train_id: int
    journey_date: date
    status: str

    class Config:
        orm_mode= True
        