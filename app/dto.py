# data transfer objects - simple objects representing the models
from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Product():
    name: str
    description: str
    brand: str
    id: Optional[int] = None


@dataclass
class Station():
    name: str
    location: str
    id: Optional[int] = None


@dataclass
class Ticket():
    date: datetime
    quantity: int
    station: Station
    product: Product
    id: Optional[int] = None
    fulfilled: Optional[bool] = False
    out_of_stock: Optional[bool] = False
    note: Optional[str] = ""


@dataclass
class TicketFormSubmission():
    station_id: int
    product_id: int
    quantity: int
    note: str
