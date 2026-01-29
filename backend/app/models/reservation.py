from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, String,
    UniqueConstraint
)
from sqlalchemy.sql import func
from app.core.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"),nullable =False)
    schedule_id = Column(Integer, ForeignKey("train_schedules.id"),nullable=False)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable = False)

    from_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    to_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)

    status = Column(String(20),default="BOOKED")
    booked_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("schedule_id","seat_id", name="uq_schedule_seat"),
    )