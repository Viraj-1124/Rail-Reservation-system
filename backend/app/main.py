from fastapi import FastAPI,status, Depends, HTTPException
from app.models.users import User
from app.core.database import engine, SessionLocal, Base
from app.auth.securities import hash_password
from app.api.auth import router
from app.api.stations import station_router
from app.api.trains import train_router
from app.api.routes import route_router
from app.api.train_schedules import train_schedule_router
from app.api.coach import coach_router 
from app.api.seat import seat_router
from app.api.search import router as search_router
from app.api.availability import router as availability_router
from app.api.reservation import router as reservation_router
from sqlalchemy.orm import Session
from app.core.database import get_db

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title = "Rail Reservation System",
    description="Backend for Indian Railway Style Booking System",
    version ="1.0.0"
)

@app.get("/")
def health_check():
    return {"ststus":status.HTTP_200_OK, "message":"Train Reservation backend is Running"}

@app.on_event("startup")
def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "ADMIN").first()
    if not admin:
        admin = User(
            name = "System Admin",
            email ="admin@railway.com",
            password_hash = hash_password("admin123"),
            role="ADMIN"
        )
        db.add(admin)
        db.commit()
    db.close()

@app.put("/make_admin")
def make_admin(email:str, db:Session =Depends(get_db)):
    user = db.query(User).filter(User.email==email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
app.include_router(router)
app.include_router(station_router)
app.include_router(train_router)
app.include_router(route_router)
app.include_router(train_schedule_router)
app.include_router(coach_router)
app.include_router(seat_router)
app.include_router(search_router)
app.include_router(availability_router)
app.include_router(reservation_router)