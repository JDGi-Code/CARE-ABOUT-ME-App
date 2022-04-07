import pytest

from app.dto import Station as StationDTO
from app.dto import Product as ProductDTO
from app.dto import Ticket as TicketDTO
from app.dto import TicketFormSubmission as RequestFormSubmissionDTO
from app.repositories.station_repository import StationRepository
from app.repositories.product_repository import ProductRepository
from app.services.ticket_service import RequestService


@pytest.mark.django_db
def test_create_request_from_submission():
    # 1. Setup - create fake station and product in db
    s = StationDTO(name='Mock1', location='Mock1Loc')
    s = StationRepository.create_or_update(s)
    p = ProductDTO(name='Mock1', description='Mock1Desc', brand='Mock1Brand')
    p = ProductRepository.create_or_update(p)
    # make a fake submission
    submission = RequestFormSubmissionDTO(station_id=s.id, product_id=p.id, quantity=5)
    # 2. Execute - call service method
    dto = RequestService.create_request_from_submission(submission)
    # 3. Assert - verify req was created, associated w correct station and product
    assert dto.id is not None


# call a service method and get back a list of dtos
@pytest.mark.django_db
def test_get_all_products_and_stations():
    # 1. Setup - create fake dtos
    s = StationDTO(name='MockStation1', location='Mock1Loc')
    s = StationRepository.create_or_update(s)
    s2 = StationDTO(name='MockStation2', location='Mock2Loc')
    s2 = StationRepository.create_or_update(s2)
    p = ProductDTO(name='MockProduct1', description='Mock1Desc', brand='Mock1Brand')
    p = ProductRepository.create_or_update(p)
    p2 = ProductDTO(name='MockProduct2', description='Mock2Desc', brand='Mock2Brand')
    p2 = ProductRepository.create_or_update(p2)
    # 2. Execute - call the service method
    dtos = RequestService.get_all_products_and_stations()
    # 3. Assert - verify that the dtos are returned
    assert len(dtos["stations"]) == 2
    assert len(dtos["products"]) == 2
    assert dtos["stations"][0].name == 'MockStation1'
    assert dtos["stations"][1].name == 'MockStation2'
    assert dtos["products"][0].name == 'MockProduct1'
    assert dtos["products"][1].name == 'MockProduct2'
