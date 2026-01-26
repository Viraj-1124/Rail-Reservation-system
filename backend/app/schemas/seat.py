from pydantic import BaseModel

class SeatResponse(BaseModel):
    id: int
    coach_id: int
    seat_number: int

    class Config:
        from_attributes = True