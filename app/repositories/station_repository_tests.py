import pytest

from app.repositories.station_repository import StationRepository
from app.models import Station
from app.dto import Station as StationDTO


# Verify that get_by_id returns the correct object matching the id, in the correct format
@pytest.mark.django_db
def test_get_by_id():
    # 1. Setup
    s = Station(name='Mock1', location='Mock1Loc')
    s.save()
    # 2. Execute
    result = StationRepository.get_by_id(id=s.id)
    # 3. Assert
    assert s.id == result.id
    assert s.name == result.name
    assert s.location == result.location


# Verify all stations were retrieved
@pytest.mark.django_db
def test_get_all():
    # 1. Setup
    Station(name='Mock1', location='Mock1Loc').save()
    Station(name='Mock2', location='Mock2Loc').save()
    # 2. Execute
    result = StationRepository.get_all()
    # 3. Assert
    assert result[0].name == 'Mock1'
    assert result[1].name == 'Mock2'
    assert len(result) == 2


# Verify objects are created
@pytest.mark.django_db
def test_create():
    # 1. Setup
    new_station = StationDTO(name='Mock1', location='Mock1Loc')
    # 2. Execute
    new_station = StationRepository.create_or_update(new_station)
    # 3. Assert
    assert new_station.id is not None
    assert Station.objects.get(id=new_station.id).name == 'Mock1'


# Verify objects are updated
@pytest.mark.django_db
def test_update():
    # 1. Setup
    new_station = StationDTO(name='Mock1', location='Mock1Loc')
    new_station = StationRepository.create_or_update(new_station)
    old_id = new_station.id
    new_station.name = 'Mock2'
    # 2. Execute
    new_station = StationRepository.create_or_update(new_station)
    # 3. Assert
    assert new_station.id == old_id
    assert Station.objects.get(id=new_station.id).name == 'Mock2'


# Verify objects are soft-deleted
@pytest.mark.django_db
def test_soft_delete():
    # 1. Setup
    new_station = StationDTO(name='Mock1', location='Mock1Loc')
    new_station = StationRepository.create_or_update(new_station)
    # 2. Execute
    StationRepository.delete(new_station)
    # 3. Assert
    with pytest.raises(Station.DoesNotExist):
        Station.objects.get(id=new_station.id)                          # filtered queryset
    assert Station.all_objects.get(id=new_station.id) is not None       # unfiltered queryset


# Verify objects are hard-deleted
@pytest.mark.django_db
def test_hard_delete():
    # 1. Setup
    new_station = StationDTO(name='Mock1', location='Mock1Loc')
    new_station = StationRepository.create_or_update(new_station)
    # 2. Execute
    StationRepository.delete(new_station, hard=True)
    # 3. Assert
    # filtered queryset
    with pytest.raises(Station.DoesNotExist):
        Station.objects.get(id=new_station.id)
    # unfiltered queryset
    with pytest.raises(Station.DoesNotExist):
        assert Station.all_objects.get(id=new_station.id)