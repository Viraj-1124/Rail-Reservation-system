from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.trains import Train
from app.services.availability_services import get_seat_availability
from app.schemas.availability import CoachAvaliability

router = APIRouter(prefix="/availability", tags=["Availability"])

@router.get("/", response_model=list[CoachAvaliability])
def check_availability(
    train_number: str = Query(...),
    db:Session = Depends(get_db)
):
    train = db.query(Train).filter(Train.train_number==train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    return get_seat_availability(db, train.id)