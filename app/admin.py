# list_display is what shows on the admin list page
# fields are what shows in each individual item

from django.contrib import admin

from .models import Product, Station, Ticket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'brand']
    list_display = ('name', 'description', 'brand')


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    fields = ['name', 'location']
    list_display = ('name', 'location')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ['station', 'product', 'quantity', 'fulfilled', 'out_of_stock']
    list_display = ('date', 'station', 'fulfilled', 'out_of_stock')
