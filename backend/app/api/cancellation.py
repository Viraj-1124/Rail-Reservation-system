from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependenties import get_current_user
from app.services.cancellation_services import cancel_reservation
from app.schemas.cancellation import CancellationResponse

router = APIRouter(prefix="/reservations", tags=["Cancellations"])

@router.delete("{/reservation_id}", response_model=CancellationResponse)
def cancel_ticket(
    reservation_id:int,
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cancel_reservation(
        db=db,
        reservation_id=reservation_id,
        current_user_id=current_user.id,
        is_admin= (current_user.role=="ADMIN")
    )