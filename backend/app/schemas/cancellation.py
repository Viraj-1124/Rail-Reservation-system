from pydantic import BaseModel

class CancellationResponse(BaseModel):
    reservation_id: int
    status: str
    message: str