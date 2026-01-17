from pydantic import BaseModel

class StationCreate(BaseModel):
    name: str
    code: str
    city: str

class StationResponse(BaseModel):
    id: int
    name: str
    code: str
    city: str

    class Config:
        orm_mode = True