from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date

from app.models.reservation import Reservation
from app.models.train_shedule import TrainSchedule

def cancel_reservation(
    db: Session,
    reservation_id: int,
    current_user_id: int,
    is_admin: bool
):

    reservation = (
        db.query(Reservation)
        .filter(Reservation.id == reservation_id)
        .with_for_update()
        .first()
    )

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if not is_admin and reservation.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not allowed to cancel this ticket")

    if reservation.status == "CANCELLED":
        raise HTTPException(status_code=409, detail="Ticket already cancelled")

    schedule = db.query(TrainSchedule).filter(
        TrainSchedule.id == reservation.schedule_id
    ).first()

    if not schedule:
        raise HTTPException(status_code=400, detail="Invalid train schedule")

    if schedule.journey_date <= date.today():
        raise HTTPException(
            status_code=400,
            detail="Journey already started or completed. Cancellation not allowed"
        )

    reservation.status = "CANCELLED"

    db.commit()         
    db.refresh(reservation)

    return {
        "reservation_id": reservation_id,
        "status": "CANCELLED",
        "message": "Ticket cancelled successfully"
    }
