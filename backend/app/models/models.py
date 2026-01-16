from sqlalchemy import Column,Integer,DateTime,String
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    password_hash = Column(String, nullable=False)
    user = Column(String, default="USER")
    created_at = Column(DateTime(timezone=True),server_default=func.now())