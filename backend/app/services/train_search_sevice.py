from sqlalchemy.orm import Session, aliased
from app.models.trains import Train
from app.models.route import Route
from app.models.stations import Station
from app.models.train_shedule import TrainSchedule
from datetime import date


def search_trains(db:Session, from_code:str, to_code:str, journey_date:date):
    SourceStation = aliased(Station)
    DestStation = aliased(Station)
    SourceRoute = aliased(Route)
    DestRoute = aliased(Route)

    query = (
        db.query(
            Train.id,
            Train.train_name,
            Train.train_number,
            SourceRoute.departure_time.label("source_departure"),
            SourceRoute.arrival_time.label("destination_arrival")
        )
        .join(TrainSchedule, TrainSchedule.train_id==Train.id)
        .join(SourceRoute, SourceRoute.train_id == Train.id)
        .join(DestRoute, DestRoute.train_id == Train.id)
        .join(SourceStation, SourceStation.id==SourceRoute.station_id)
        .join(DestStation, DestStation.id == DestRoute.station_id)
        .filter(
            SourceStation.code == from_code,
            DestStation.code == to_code,
            SourceRoute.sequence < DestRoute.sequence,
            TrainSchedule.journey_date == journey_date,
            TrainSchedule.status == "ACTIVE"
        )
    )

    return query.all()