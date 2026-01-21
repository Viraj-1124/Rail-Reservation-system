from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.models.train_shedule import TrainSchedule
from app.models.trains import Train
from app.schemas.train_schedule import TrainScheduleCreate, TrainScheduleResponse 
from app.auth.dependenties import admin_only

train_schedule_router = APIRouter(prefix="/schedule", tags=["Train Schedule"])

@train_schedule_router.post("/", dependencies=[Depends(admin_only)])
def create_schedule(data: TrainScheduleCreate, db:Session = Depends(get_db)):
    train = db.query(Train).filter(Train.train_number == data.train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    exists = db.query(TrainSchedule).filter(
        TrainSchedule.train_id == train.id,
        TrainSchedule.journey_date == data.journey_date
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Schedule already exists")
    
    schedule = TrainSchedule(
        train_id = train.id,
        journey_date = data.journey_date,
        status = data.status
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@train_schedule_router.get("/",response_model=list[TrainScheduleResponse])
def get_schedule(
    journey_date: date=Query(..., description="Journey date in YYYY-MM-DD format"),
    db: Session=Depends(get_db)
):
    return db.query(TrainSchedule).filter(
        TrainSchedule.journey_date ==journey_date,
        TrainSchedule.status == "ACTIVE"
    ).all()
