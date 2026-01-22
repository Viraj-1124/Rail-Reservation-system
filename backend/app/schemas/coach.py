from pydantic import BaseModel

class CoachCreate(BaseModel):
    train_number : str
    coach_type : str
    total_seats : int


class CoachResponse(BaseModel):
    id: int
    train_id: int
    coach_type: str
    total_seats: int

    class Config:
        from_attributes = True