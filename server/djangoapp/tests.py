from django.test import TestCase

from .models import CarMake, Dealer, Review
from .views import analyze_sentiment


class SentimentTests(TestCase):
    def test_positive_sentiment(self):
        self.assertEqual(analyze_sentiment("Fantastic services"), "positive")

    def test_negative_sentiment(self):
        self.assertEqual(analyze_sentiment("Terrible and rude staff"), "negative")

    def test_neutral_sentiment(self):
        self.assertEqual(analyze_sentiment("I visited the dealership"), "neutral")


class ApiTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(
            full_name="Test Motors", short_name="Test Motors",
            address="1 Test St", city="Topeka", state="Kansas", zip="66603",
        )
        self.make = CarMake.objects.create(name="Toyota")
        Review.objects.create(
            dealer=self.dealer, name="Alice", review="Great service",
            sentiment="positive",
        )

    def test_get_dealers(self):
        response = self.client.get("/djangoapp/get_dealers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_get_dealers_by_state(self):
        response = self.client.get("/djangoapp/get_dealers/Kansas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_get_dealer_by_id(self):
        response = self.client.get(f"/djangoapp/dealer/{self.dealer.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["dealer"]["full_name"], "Test Motors")

    def test_get_dealer_reviews(self):
        response = self.client.get(f"/djangoapp/reviews/dealer/{self.dealer.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["reviews"]), 1)

    def test_get_cars(self):
        response = self.client.get("/djangoapp/get_cars/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["car_makes"][0]["make"], "Toyota")

    def test_analyze_endpoint(self):
        response = self.client.get("/djangoapp/analyze/Fantastic%20services")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "positive")
