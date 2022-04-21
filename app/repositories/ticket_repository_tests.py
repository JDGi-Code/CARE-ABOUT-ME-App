import pytest

from datetime import date
from app.repositories.ticket_repository import TicketRepository
from app.models import Ticket
from app.models import Station
from app.models import Product
from app.dto import Station as StationDTO
from app.dto import Product as ProductDTO
from app.dto import Ticket as TicketDTO


# Verify that get_by_id returns the correct object matching the id, in the correct format
@pytest.mark.django_db
def test_get_by_id():
    # 1. Setup
    s = Station(name='Mock1', location='Mock1Loc')
    s.save()
    p = Product(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    p.save()
    rq = Ticket(date=date.today(), quantity=1, fulfilled=False, station_id=s.id, product_id=p.id)
    rq.save()
    # 2. Execute
    result = TicketRepository.get_by_id(id=rq.id)
    # 3. Assert
    assert rq.id == result.id
    assert rq.date == result.date
    assert rq.fulfilled == result.fulfilled
    assert rq.station_id == result.station.id
    assert rq.product_id == result.product.id


# Verify that get_by_id returns the correct object matching the id, in the correct format
@pytest.mark.django_db
def test_note_retrieval():
    # 1. Setup
    s = Station(name='Mock1', location='Mock1Loc')
    s.save()
    p = Product(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    p.save()
    n = "mock note"
    rq = Ticket(date=date.today(), quantity=1, fulfilled=False, station_id=s.id, product_id=p.id, note=n)
    rq.save()
    # 2. Execute
    result = TicketRepository.get_by_id(id=rq.id)
    # 3. Assert
    assert rq.note == n


# Verify all requests were retrieved
@pytest.mark.django_db
def test_get_all():
    # 1. Setup
    s = Station(name='Mock1', location='Mock1Loc')
    s.save()
    p = Product(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    p.save()
    rq1 = Ticket(date=date.today(), quantity=1, fulfilled=False, station_id=s.id, product_id=p.id)
    rq1.save()
    rq2 = Ticket(date=date.today(), quantity=1, fulfilled=False, station_id=s.id, product_id=p.id)
    rq2.save()
    # 2. Execute
    result = TicketRepository.get_all()
    # 3. Assert
    assert result[0].id == rq1.id
    assert result[1].id == rq2.id
    assert result[0].station.id == rq1.station_id
    assert result[0].product.id == rq1.product_id
    assert result[1].station.id == rq1.station_id
    assert result[1].product.id == rq1.product_id
    assert len(result) == 2


# Verify objects are created
@pytest.mark.django_db
def test_create():
    # 1. Setup
    s = StationDTO(name='Mock1', location='Mock1Loc')
    p = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    dto = TicketDTO(date=date.today(), quantity=1, fulfilled=False, station=s, product=p)
    # 2. Execute
    new_request = TicketRepository.create_or_update(dto)
    # 3. Assert
    assert new_request.id is not None
    assert new_request.date == dto.date


# Verify objects are created
@pytest.mark.django_db
def test_create_with_note():
    # 1. Setup
    s = StationDTO(name='Mock1', location='Mock1Loc')
    p = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    n = "mock note"
    dto = TicketDTO(date=date.today(), quantity=1, fulfilled=False, station=s, product=p, note=n)
    # 2. Execute
    new_request = TicketRepository.create_or_update(dto)
    # 3. Assert
    assert new_request.note == n


# Verify objects are updated
@pytest.mark.django_db
def test_update():
    # 1. Setup
    s = StationDTO(name='Mock1', location='Mock1Loc')
    p = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    dto = TicketDTO(date=date.today(), quantity=1, fulfilled=False, station=s, product=p)
    dto = TicketRepository.create_or_update(dto)
    old_id = dto.id
    dto.quantity = 3
    # 2. Execute
    dto = TicketRepository.create_or_update(dto)
    # 3. Assert
    assert dto.id == old_id
    assert Ticket.objects.get(id=dto.id).quantity == 3


# Verify objects are hard-deleted
@pytest.mark.django_db
def test_hard_delete():
    # 1. Setup
    s = StationDTO(name='Mock1', location='Mock1Loc')
    p = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    dto = TicketDTO(date=date.today(), quantity=1, fulfilled=False, station=s, product=p)
    dto = TicketRepository.create_or_update(dto)
    # 2. Execute
    TicketRepository.delete(dto)
    # 3. Assert
    with pytest.raises(Ticket.DoesNotExist):
        Ticket.objects.get(id=dto.id)
