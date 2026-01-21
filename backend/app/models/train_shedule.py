from sqlalchemy import Integer, Column, ForeignKey,  Date, String, UniqueConstraint, Index
from app.core.database import Base

class TrainSchedule(Base):
    __tablename__ = "train_schedules"

    id = Column(Integer, primary_key = True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="CASCADE"), nullable=False)
    journey_date = Column(Date,nullable=False)
    status = Column(String(20),default="ACTIVE")

    __table_args__ = (
        UniqueConstraint("train_id", "journey_date", name="uq_train_date"),
        Index("idx_schedule_train", "train_id"),
        Index("idx_schedule_date", "journey_date")
    )