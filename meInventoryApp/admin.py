from django.contrib import admin

from app.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (Ticket.objects.date, Ticket.objects.station, Ticket.objects.fulfilled)


admin.site.register(Ticket, TicketAdmin)
