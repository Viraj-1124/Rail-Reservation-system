from pydantic import BaseModel

class TrainCreate(BaseModel):
    train_number: str
    train_name: str


class TrainResponse(BaseModel):
    id: int
    train_number: str
    train_name: str

    class config:
        orm_mode =True