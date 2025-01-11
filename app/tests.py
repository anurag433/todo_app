from django.test import TestCase

# Create your tests here.
class TestTest(TestCase):
    def test_test(self):
        resp = self.client.get("/")