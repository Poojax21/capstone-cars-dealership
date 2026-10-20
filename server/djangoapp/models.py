from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    year = models.IntegerField(default=2020)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealer(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    purchase = models.BooleanField(default=False)
    review = models.TextField()
    sentiment = models.CharField(max_length=20, default="neutral")
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"Review by {self.name} for {self.dealer.short_name}"
