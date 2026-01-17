from sqlalchemy import Column,String,Integer
from app.core.database import Base

class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True)
    train_number = Column(String(20), unique=True, index=True, nullable=False)
    train_name = Column(String(100), nullable=False)