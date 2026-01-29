from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependenties import get_current_user
from app.schemas.reservation import ReservationCreate
from app.services.reservation_services import book_seat

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/book")
def book_seat_api(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return book_seat(
        db=db,
        user_id=current_user.id,
        schedule_id=data.schedule_id,
        coach_type=data.coach_type,
        from_code=data.from_station_code,
        to_code=data.to_station_code
    )