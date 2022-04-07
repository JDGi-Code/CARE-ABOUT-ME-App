import pytest

from app.services.auth_service import AuthService
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from unittest import mock


# Fake user for the purpose of testing auth
class MockUser(mock.Mock):
    is_authenticated = False

    def __init__(self, is_authenticated):
        super().__init__()
        self.is_authenticated = is_authenticated


# Fake request session for the purpose of testing auth
class MockRequest(mock.Mock):
    user = None

    def __init__(self, is_authenticated = False):
        super().__init__()
        self.user = MockUser(is_authenticated = is_authenticated)


# Test that the user is logged in
@pytest.mark.django_db
def test_user_is_logged_in():
    # 1. Create a user
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'secret')
    user.save()
    # 2. Authenticate
    user = authenticate(username='john', password='secret')
    # Make a fake request object and attach user to it; or have user persist in session & pass in session
    request = MockRequest()
    request.user = user
    result = AuthService().user_is_logged_in(request)
    assert result is True


# Test that the user is not logged in
@pytest.mark.django_db
def test_user_is_not_logged_in():
    # Make a fake request object and attach user to it; or have user persist in session & pass in session
    request = MockRequest()
    result = AuthService().user_is_logged_in(request)
    assert result is False
