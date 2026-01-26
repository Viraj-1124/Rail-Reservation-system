from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.services.train_search_sevice import search_trains
from app.schemas.search import TrainSearchResult

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/trains",response_model=list[TrainSearchResult])
def search_train_api(
    from_station: str = Query(..., alias="from"),
    to_station: str = Query(..., alias="to"),
    journey_date: str= Query(...),
    db:Session =Depends(get_db)
):
    return search_trains(db, from_station, to_station, journey_date)