from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models import (
    TrainSchedule, Route, Station,
    Coach, Seat, Reservation
)

def book_seat(
    db: Session,
    user_id: int,
    schedule_id: int,
    coach_type: str,
    from_code: str,
    to_code: str
):
    try:
        with db.begin():

            schedule = db.query(TrainSchedule).filter(
                TrainSchedule.id == schedule_id,
                TrainSchedule.status == "ACTIVE"
            ).first()

            if not schedule:
                raise HTTPException(status_code=404, detail="Invalid or Inactive schedule")
            
            from_station=db.query(Station).filter(
                Station.code == from_code
            ).first()
            to_station = db.query(Station).filter(
                Station.code==to_code
            ).first()

            if not from_station or not to_station:
                raise HTTPException(status_code=404, detail="Station not found")
            

            from_route = db.query(Route).filter(
                Route.train_id == schedule.train_id,
                Route.station_id == from_station.id
            ).first()
            to_route = db.query(Route).filter(
                Route.train_id == schedule.train_id,
                Route.station_id == to_station.id
            ).first()

            if not from_route or not to_route:
                raise HTTPException(status_code=400, detail="Train does not pass from that stations")
            

            if from_route.sequence >= to_route.sequence:
                raise HTTPException(status_code=400, detail="Invalid journey directon")
            

            coach = db.query(Coach).filter(
                Coach.train_id == schedule.train_id,
                Coach.coach_type == coach_type
            ).first()

            if not coach:
                raise HTTPException(status_code=404, detail="Coach not found")
            

            seat = (
                db.query(Seat)
                .filter(Seat.coach_id ==  coach.id)
                .filter(
                    ~Seat.id.in_(
                        db.query(Reservation.seat_id).filter(
                            Reservation.schedule_id == schedule_id,
                            Reservation.status == "BOOKED"
                        )
                    )
                ).with_for_update()
                .first()
            )

            if not seat:
                raise HTTPException(409,"Seats not available")
            
            reservation = Reservation(
                user_id = user_id,
                schedule_id = schedule_id,
                coach_id = coach.id,
                seat_id = seat.id,
                from_station_id = from_station.id,
                to_station_id = to_station.id
            )

            db.add(reservation)
            return {"message":"Seat booked Successfully"}
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Seat just got booked by an another user")