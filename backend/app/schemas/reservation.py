from pydantic import BaseModel

class ReservationCreate(BaseModel):
    schedule_id: int
    coach_type: str
    from_station_code: str
    to_station_code: str
