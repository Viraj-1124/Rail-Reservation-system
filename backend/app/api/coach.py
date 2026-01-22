from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.coach import Coach
from app.models.trains import Train
from app.schemas.coach import CoachCreate, CoachResponse
from app.auth.dependenties import admin_only

coach_router = APIRouter(prefix="/coaches", tags=["Coaches"])


@coach_router.post("/", dependencies=[Depends(admin_only)])
def create_coach(data: CoachCreate, db:Session=Depends(get_db)):
    train = db.query(Train).filter(Train.train_number==data.train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    exists = db.query(Coach).filter(
        Coach.train_id == train.id,
        Coach.coach_type == data.coach_type
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Coach for that train already exists")
    
    coach = Coach(
        train_id = train.id,
        coach_type = data.coach_type,
        total_seats = data.total_seats
    )

    db.add(coach)
    db.commit()
    db.refresh(coach)
    return coach


@coach_router.get("/train/{train_number}", response_model=list[CoachResponse])
def get_train_coaches(train_number: str, db:Session = Depends(get_db)):
    train = db.query(Train).filter(Train.train_number==train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    return db.query(Coach).filter(Coach.train_id==train.id).all()