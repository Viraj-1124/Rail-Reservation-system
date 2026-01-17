from sqlalchemy import Integer, Column , String
from app.core.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10),unique=True, index=True, nullable=False)
    city = Column(String(50),nullable=False)