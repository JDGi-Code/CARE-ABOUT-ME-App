from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View


class AuthView(View):
    # Shows the login page
    def get(self, request, *args, **kwargs):
        return render(request, 'app/auth/login.html')

    # Handles a login attempt
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            response = redirect('/')
            return response
        else:
            # Return an 'invalid login' error message.
            response = redirect('/login')
            return response
