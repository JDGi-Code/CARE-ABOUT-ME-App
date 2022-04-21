from seleniumbase import BaseCase
from django.test import LiveServerTestCase
from app.tests.utils import create_session_cookie
from app.models import Ticket


# verify that the form allows the user to enter information, submits it and creates a request
class UserFunctionTest(LiveServerTestCase, BaseCase):
    # setup for test
    def setUp(self):
        super().setUp()
        cookie = create_session_cookie(username='superadmin', password='superadmin')
        self.open('http://127.0.0.1:8000/')
        self.type("input#username", "superadmin")
        self.type("input#password", "superadmin")
        self.click("input[type=submit]")
        self.wait_for_element("#station_id")

    # test form load
    def test_load_ticket_form(self):
        url = 'http://127.0.0.1:8000/'
        self.open(url)
        self.assert_title("Thrive M.E. Inventory App")
        self.assert_text("Thrive M.E. Inventory App Station Ticket Form", "h1")

    # enter form data and submit
    def test_form_submit(self):
        url = 'http://127.0.0.1:8000/'
        self.open(url)
        self.type("#station_id", "1")
        self.type("#product_id", "3")
        self.type("input#quantity", "5")
        self.type("textarea#note", "mock note")
        self.is_text_visible("mock note", "body")
        self.click("input[type=submit]")
        self.is_text_visible("Ticket(date=datetime.date(", "body")
