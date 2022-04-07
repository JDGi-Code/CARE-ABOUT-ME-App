from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from app.services.auth_service import AuthService
from app.dto import *
from app.services.ticket_service import RequestService


class TicketView(View):
    # Show the request page
    def get(self, request):
        if AuthService().user_is_logged_in(request):
            objects = RequestService.get_all_products_and_stations()
            return render(request, 'app/ticket_form.html', {'username': request.user.email, 'stations': objects['stations'], 'products': objects['products']})
        else:
            return render(request, 'app/auth/login.html')

    # Handles a product request action - constructs a request DTO
    def post(self, request):
        # pull out product station and quantity in submission
        # store the data as a request object
        new_submission = TicketFormSubmission(station_id=request.POST['station_id'], product_id=request.POST['product_id'], quantity=request.POST['quantity'])
        # give submission to service to create it
        RequestService.create_request_from_submission(new_submission)
        # flash success message
        messages.success(request, 'Ticket submitted!')
        # refresh the page and show the form again
        return self.get(request)
