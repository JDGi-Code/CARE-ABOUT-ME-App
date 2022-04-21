from app.models import Ticket
from app.repositories.station_repository import StationRepository
from app.repositories.product_repository import ProductRepository
from app.dto import Ticket as TicketDTO
from typing import List


class TicketRepository():
    @classmethod
    def get_by_id(cls, id: int) -> TicketDTO:
        return Ticket.objects.get(id=id).to_dto()

    @classmethod
    def get_all(cls) -> List[TicketDTO]:
        all_requests = Ticket.objects.all()
        return [x.to_dto() for x in all_requests]

    @classmethod
    def create_or_update(cls, request: TicketDTO) -> TicketDTO:
        if request.id:
            r = Ticket.objects.get(id=request.id)
        else:
            r = Ticket()
        r.date = request.date
        r.quantity = request.quantity
        r.fulfilled = request.fulfilled
        r.note = request.note
        # give station_id to to station create_or_update method
        r.station_id = StationRepository.create_or_update(request.station).id
        r.product_id = ProductRepository.create_or_update(request.product).id
        r.save()
        return r.to_dto()

    @classmethod
    def delete(cls, request: TicketDTO) -> bool:
        r = Ticket.objects.get(id=request.id)
        return r.delete()
