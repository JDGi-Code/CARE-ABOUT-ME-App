from datetime import date
from app.dto import TicketFormSubmission
from app.repositories.station_repository import StationRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.ticket_repository import TicketRepository
from app.dto import Ticket as TicketDTO


class RequestService:

    @classmethod
    def create_request_from_submission(cls, submission: TicketFormSubmission) -> TicketDTO:
        station = StationRepository.get_by_id(submission.station_id)
        product = ProductRepository.get_by_id(submission.product_id)
        request_dto = TicketDTO(date=date.today(), quantity=submission.quantity, station=station, product=product, note=submission.note)
        return TicketRepository.create_or_update(request_dto)

    # return a list of all product and station objects
    @classmethod
    def get_all_products_and_stations(cls):
        stations = StationRepository.get_all()
        products = ProductRepository.get_all()
        return {"stations": stations, "products": products}
