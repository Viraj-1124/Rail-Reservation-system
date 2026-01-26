from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependenties import admin_only
from app.models.seat import Seat
from app.models.trains import Train
from app.models.coach import Coach
from app.schemas.seat import SeatResponse

seat_router = APIRouter(prefix="/seats", tags=["Seats"])

@seat_router.post("/generate/{train_number}/{coach_type}", dependencies=[Depends(admin_only)])
def generate_seats(train_number: str,coach_type:str, db:Session=Depends(get_db)):
    train = db.query(Train).filter(Train.train_number==train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    coach = db.query(Coach).filter(
        Coach.train_id == train.id,
        Coach.coach_type == coach_type
    ).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    existing = db.query(Seat).filter(Seat.coach_id==coach.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Seats already generated")
    
    seats = [
        Seat(coach_id = coach.id, seat_number = i)
        for i in range(1, coach.total_seats+1)
    ]

    db.bulk_save_objects(seats)
    db.commit()
    return {"message": f"{coach.total_seats} seats generated for {coach_type} coach"}


@seat_router.get("/coach/{train_number}/{coach_type}", response_model=list[SeatResponse])
def get_seats(train_number:str, coach_type:str, db:Session = Depends(get_db)):
    train = db.query(Train).filter(Train.train_number==train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    coach = db.query(Coach).filter(
        Coach.train_id == train.id,
        Coach.coach_type == coach_type
    ).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    return db.query(Seat).filter(Seat.coach_id == coach.id).all()