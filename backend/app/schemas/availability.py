from pydantic import BaseModel

class CoachAvaliability(BaseModel):
    coach_type: str
    total_seats: str
    booked_seats: str
    available_seats: str