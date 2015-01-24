from app.views.user_view import UserView
from django.test import Client, TestCase

class TestUserView(TestCase):
    "UserView Test"
    def setUp(self):
        self.a = 1

    def tearDown(self):
        del self.a

    def test_basic1(self):
        assert self.a != 2

    def test_basic2(self):
        "Basic2 with setup"
        assert self.a != 2 
