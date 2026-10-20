import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel, Dealer, Review
from djangoapp.views import analyze_sentiment

DEALERS = [
    ("Kansas City Auto Mall", "KC Auto Mall", "1200 Main Street", "Kansas City", "Kansas", "66101", 39.1141, -94.6275),
    ("Wichita Motors", "Wichita Motors", "455 N Broadway", "Wichita", "Kansas", "67202", 37.6872, -97.3301),
    ("Topeka Car Center", "Topeka Cars", "800 SW Kansas Ave", "Topeka", "Kansas", "66603", 39.0473, -95.6752),
    ("Dallas Auto Group", "Dallas Auto", "1500 Commerce St", "Dallas", "Texas", "75201", 32.7767, -96.7970),
    ("Austin Wheels", "Austin Wheels", "600 Congress Ave", "Austin", "Texas", "78701", 30.2672, -97.7431),
    ("Chicago Motors", "Chicago Motors", "233 S Wacker Dr", "Chicago", "Illinois", "60606", 41.8789, -87.6359),
    ("Springfield Auto", "Springfield Auto", "100 E Monroe St", "Springfield", "Illinois", "62701", 39.7817, -89.6501),
    ("Denver Dealership", "Denver Dealer", "1700 Lincoln St", "Denver", "Colorado", "80203", 39.7392, -104.9903),
    ("Miami Auto Plaza", "Miami Auto", "200 S Biscayne Blvd", "Miami", "Florida", "33131", 25.7617, -80.1918),
    ("Phoenix Car Hub", "Phoenix Cars", "1 E Washington St", "Phoenix", "Arizona", "85004", 33.4484, -112.0740),
]

CARS = {
    "Toyota": [("Corolla", "Sedan", 2022), ("Camry", "Sedan", 2023), ("RAV4", "SUV", 2022)],
    "Honda": [("Civic", "Sedan", 2021), ("CR-V", "SUV", 2023), ("Accord", "Sedan", 2022)],
    "Ford": [("F-150", "Truck", 2023), ("Mustang", "Coupe", 2022), ("Escape", "SUV", 2021)],
    "Tesla": [("Model 3", "Sedan", 2023), ("Model Y", "SUV", 2023)],
    "BMW": [("3 Series", "Sedan", 2022), ("X5", "SUV", 2023)],
}

REVIEWS = [
    (1, "John Doe", True, "Fantastic services", 2023, "Toyota", "Camry"),
    (1, "Jane Smith", True, "Great experience and very helpful staff", 2022, "Honda", "Civic"),
    (2, "Mike Brown", False, "The waiting time was too long and staff were rude", 2023, "Ford", "F-150"),
    (2, "Sarah Lee", True, "Excellent dealership, highly recommend", 2022, "Tesla", "Model 3"),
    (4, "Chris Green", True, "Smooth purchase, friendly people", 2023, "BMW", "X5"),
]


class Command(BaseCommand):
    help = "Seed the database with dealers, cars, reviews and demo users."

    def handle(self, *args, **options):
        Dealer.objects.all().delete()
        CarMake.objects.all().delete()
        Review.objects.all().delete()
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name IN "
                "('djangoapp_dealer','djangoapp_carmake','djangoapp_carmodel','djangoapp_review')"
            )

        dealer_objs = []
        for d in DEALERS:
            dealer_objs.append(Dealer.objects.create(
                full_name=d[0], short_name=d[1], address=d[2], city=d[3],
                state=d[4], zip=d[5], latitude=d[6], longitude=d[7],
            ))

        for make_name, models in CARS.items():
            make = CarMake.objects.create(name=make_name)
            for name, ctype, year in models:
                CarModel.objects.create(car_make=make, name=name, type=ctype, year=year)

        for dealer_id, name, purchase, text, year, make, model in REVIEWS:
            Review.objects.create(
                dealer=dealer_objs[dealer_id - 1],
                name=name,
                purchase=purchase,
                review=text,
                sentiment=analyze_sentiment(text),
                purchase_date=datetime.date(year, 6, 15),
                car_make=make,
                car_model=model,
                car_year=str(year),
            )

        if not User.objects.filter(username="root").exists():
            User.objects.create_superuser("root", "root@carsdealership.com", "root")
        if not User.objects.filter(username="testuser").exists():
            User.objects.create_user("testuser", "test@example.com", "testpass123")

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(dealer_objs)} dealers, {CarMake.objects.count()} makes, "
            f"{Review.objects.count()} reviews, users root/root and testuser/testpass123."
        ))
