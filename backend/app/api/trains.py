from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.trains import Train
from app.schemas.trains import TrainCreate,TrainResponse
from app.auth.dependenties import admin_only

train_router = APIRouter(prefix="/trains",tags=["Trains"])

@train_router.post("/", dependencies=[Depends(admin_only)])
def create_train(data:TrainCreate, db:Session=Depends(get_db)):
    if db.query(Train).filter(Train.train_number==data.train_number).first():
        raise HTTPException(status_code=400,detail="Train already exist")
    
    train = Train(**data.dict())
    db.add(train)
    db.commit()
    db.refresh(train)
    return train


@train_router.get("/",response_model=list[TrainResponse])
def get_train(db:Session = Depends(get_db)):
    return db.query(Train).all()


@train_router.put("/{train_number}",dependencies=[Depends(admin_only)])
def update_train(train_number: str, data: TrainCreate, db:Session = Depends(get_db)):
    train = db.query(Train).filter(Train.train_number == train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    train.train_number = data.train_number
    train.train_name = data.train_name
    db.commit()
    return train


@train_router.delete("/{train_number}",dependencies=[Depends(admin_only)])
def delete_train(train_number: str,db:Session=Depends(get_db)):
    train = db.query(Train).filter(Train.train_number == train_number).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    db.delete(train)
    db.commit()
    return {"message": "Train deleted"}