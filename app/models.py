from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from app.dto import Product as ProductDTO
from app.dto import Station as StationDTO
from app.dto import Ticket as TicketDTO


# Query Set
class SoftDeletionQuerySet(models.QuerySet):
    # bulk delete a queryset - bypasses an individual object's delete method
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    # removes queryset from database
    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    # alive and dead are helpers
    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

    # # return all objects that are soft-deleted
    # def get_deleted(self):
    #     self.filter()


# Manager
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    # only return what hasn't been deleted
    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    # "true" delete
    def hard_delete(self):
        return self.get_queryset().hard_delete()


# SoftDeletionModel
class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    # calling .delete() on an object inheriting this model will softDelete the object
    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    # really, truly delete something from the database
    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


# Station has name, location
class Station(SoftDeletionModel):
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=255)

    def to_dto(self):
        return StationDTO(id=self.id, name=self.name, location=self.location)

    def __str__(self):
        return "" + str(self.name) + " (" + str(self.location) + ")"


# Product, Station, Ticket
# Products has name, desc, brand
class Product(SoftDeletionModel):
    name = models.CharField(max_length=45)
    description = models.TextField()
    brand = models.CharField(max_length=45)

    def to_dto(self):
        return ProductDTO(id=self.id, name=self.name, description=self.description, brand=self.brand)

    def __str__(self):
        return "" + str(self.name) + " (" + str(self.brand) + ")" + "\nDescription: " + str(self.description)


# Ticket has date, quantity, fulfilled, station, product, picture
# station and product link to the other models
# Many-to-One: One request can have one station and one product,
# but each product and station can be part of many requests
class Ticket(models.Model):
    date = models.DateField(auto_now=True)
    # When the station is deleted, all the requests for that station are also deleted
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    # When a product is deleted, all requests for that product are also deleted
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=(MinValueValidator(1),))
    fulfilled = models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return "" + str(self.date) + " - " + self.station.name

    def to_dto(self):
        return TicketDTO(id=self.id, date=self.date, quantity=self.quantity, fulfilled=self.fulfilled, station=self.station.to_dto(), product=self.product.to_dto(), out_of_stock=self.out_of_stock)
