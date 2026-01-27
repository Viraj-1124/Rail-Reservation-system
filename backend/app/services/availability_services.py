from sqlalchemy.orm import Session
from app.models.coach import Coach
from app.models.seat import Seat


def get_seat_availability(
    db:Session,
    train_id: int
):
    coaches = db.query(Coach).filter(Coach.train_id==train_id),all()
    availiability = []

    for coach in coaches:
        total_seats = db.query(Seat).filter(
            Seat.coach_id == coach.id
        ).count()

    booked_seats = 0

    availiability.append({
        "coach_type": coach.coach_type,
        "total_seats": total_seats,
        "booked_seats": booked_seats,
        "availaible_seats": total_seats - booked_seats   
    }
    )

    return availiability