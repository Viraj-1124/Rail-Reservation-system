from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.stations import Station
from app.schemas.stations import StationCreate, StationResponse
from app.auth.dependenties import admin_only

station_router = APIRouter(prefix="/stations", tags=["stations"])

@station_router.post("/",dependencies=[Depends(admin_only)])
def create_station(data: StationCreate, db: Session = Depends(get_db)):
    if db.query(Station).filter(Station.code==data.code).first():
        raise HTTPException(status_code=400, detail="Station code already exists")
    
    station = Station(**data.model_dump())
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


@station_router.post("/{station_id}",dependencies=[Depends(admin_only)])
def update_station(station_code: int, data: StationCreate, db:Session = Depends(get_db)):
    station = db.query(Station).filter(Station.code ==station_code).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    for key,value in data.dict().items():
        setattr(station,key,value)

    db.commit()
    return station

@station_router.delete("/{station_code}",dependencies=[Depends(admin_only)])
def delelte_station(station_code: int, db:Session = Depends(get_db)):
    station = db.query(Station).filter(Station.code ==station_code).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    db.delete(station)
    db.commit()
    return {"message": "Station deleted"}


@station_router.get("/",response_model=list[StationResponse])
def get_station(db:Session = Depends(get_db)):
    return db.query(Station).all()


@station_router.get("/{station_id}")
def search_station(station_code: int, db:Session = Depends(get_db)):
    station = db.query(Station).filter(station_code==Station.code).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@station_router.get("/{station_name}")
def search_station_by_name(station_name: str, db:Session = Depends(get_db)):
    station = db.query(Station).filter(station_name==Station.name).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station