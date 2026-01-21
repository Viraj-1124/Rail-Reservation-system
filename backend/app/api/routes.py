from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.route import Route
from app.models.trains import Train
from app.models.stations import Station
from app.schemas.route import RouteCreate
from app.auth.dependenties import admin_only

route_router = APIRouter(prefix="/routes", tags=["Routes"])

@route_router.post("/", dependencies=[Depends(admin_only)])
def create_route(data: RouteCreate, db:Session = Depends(get_db)):
    train = db.query(Train).filter(Train.train_number == data.train_number).first()
    if not train:
        raise HTTPException(status_code=404, details="Train not found")
    
    station = db.query(Station).filter(Station.code == data.station_code).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    

    existing = db.query(Route).filter(
        Route.train_id == train.id,
        Route.station_id == station.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Station already in route")
    
    route = Route(
        train_id=train.id,
        station_id=station.id,
        arrival_time=data.arrival_time,
        departure_time=data.departure_time,
        day_number=data.day_number,
        sequence=data.sequence
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route


@route_router.get("/train/{train_number}")
def get_train_route(train_number: str, db:Session = Depends(get_db)):
    train = db.query(Train).filter(Train.train_number == train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    return db.query(Route).filter(
        Route.train_id == train.id
    ).order_by(
        Route.sequence
    ).all()
    