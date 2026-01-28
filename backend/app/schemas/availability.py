from pydantic import BaseModel

class CoachAvaliability(BaseModel):
    coach_type: str
    total_seats: int
    booked_seats: int
    available_seats: int