from unittest import TestCase
from fastapi.testclient import TestClient

from server import app, NUMBER_OF_PATIENTS_TO_RETURN


class TestReadRoot(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.url = "/patients"

    def test_invalid_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

    def test_with_invalid_location(self):
        response = self.client.get(self.url + "?location='invalid'")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("detail"), "Invalid location format")

    def test_without_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("detail"), "Location is required")

    def test_with_valid_location(self):
        response = self.client.get(self.url + "?location=1.0,1.0")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["data"], list)
        self.assertEqual(len(response.json()["data"]), NUMBER_OF_PATIENTS_TO_RETURN)
