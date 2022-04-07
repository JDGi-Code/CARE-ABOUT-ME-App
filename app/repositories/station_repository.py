from app.models import Station
from app.dto import Station as StationDTO
from typing import List


class StationRepository():
    @classmethod
    def get_by_id(cls, id: int) -> StationDTO:
        return Station.objects.get(id=id).to_dto()

    @classmethod
    def get_all(cls) -> List[StationDTO]:
        all_stations = Station.objects.all()
        return [x.to_dto() for x in all_stations]

    @classmethod
    def create_or_update(cls, station: StationDTO) -> StationDTO:
        if station.id:
            s = Station.objects.get(id=station.id)
        else:
            s = Station()
        s.name = station.name
        s.location = station.location
        s.save()
        return s.to_dto()

    @classmethod
    def delete(cls, station: StationDTO, hard=False) -> bool:
        s = Station.objects.get(id=station.id)
        if hard:
            return s.hard_delete()
        else:
            return s.delete()
