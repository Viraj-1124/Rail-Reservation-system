from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from app.core.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    coach_id = Column(Integer, ForeignKey("coaches.id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("coach_id", "seat_number", name="uq_coach_seat"),
        Index("idx_seat_coach", "coach_id"),
    )