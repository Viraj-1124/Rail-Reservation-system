from sqlalchemy import Integer, Column, ForeignKey, String, UniqueConstraint, Index
from app.core.database import Base

class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key = True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="CASCADE"), nullable=False)
    coach_type = Column(String(5), nullable=False)
    total_seats = Column(Integer, nullable =False)

    __table_args__ = (
        UniqueConstraint("train_id","coach_type",name="uq_train_coach"),
        Index("idx_coach_train", "train_id")
    )