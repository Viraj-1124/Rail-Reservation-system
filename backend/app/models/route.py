from sqlalchemy import Integer, ForeignKey, Time, Column
from app.core.database import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="CASCADE"), index=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"))
    arrival_time = Column(Time, nullable =True)
    departure_time = Column(Time, nullable=True)
    day_number = Column(Integer,nullable=False)
    sequence = Column(Integer, nullable=False)