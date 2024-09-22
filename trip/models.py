from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
Account = get_user_model()

class Destination(models.Model):
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.CharField(max_length=250)

class Trip(models.Model):
    trip_name = models.CharField(max_length=255)
    # destination = models.CharField(max_length=300)
    destination = models.ForeignKey(Destination, related_name="trip_destination", on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(Account, related_name="user_trip", on_delete=models.CASCADE)

class Lodge(models.Model):
    location = models.CharField(max_length=255)
    address = models.TextField()

class Activity(models.Model):
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=255)
    activity_name = models.CharField(max_length=255)  # Corrected length parameter
    activity_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.activity_name

class Transport(models.Model):
    class TransportType(models.TextChoices):
        FLIGHT = "flight", "Flight"
        BUS = "bus", "Bus"
        TRAIN = "train", "Train"
        SHIP = "ship", "Ship"
        CAR = "car", "Car"

    transport_type = models.CharField(max_length=100, choices=TransportType.choices)  # E.g., Flight, Train, Bus
    departure_location = models.CharField(max_length=255)
    arrival_location = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.transport_type} from {self.departure_location} to {self.arrival_location}"


class ItineraryItem(models.Model):
    class ItemType(models.TextChoices):
        TRANSPORT = "transport", "Transport"
        LODGE = "lodge", "Lodge"
        ACTIVITY = "activity", "Activity"

    itinerary = models.ForeignKey("Itinerary", related_name="items", on_delete=models.CASCADE)
    item_type = models.CharField(max_length=75, choices=ItemType.choices)
    lodge = models.ForeignKey(Lodge, related_name="itinerary_items", on_delete=models.SET_NULL, null=True, blank=True)
    transport = models.ForeignKey(Transport, related_name="itinerary_items", on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, related_name="itinerary_items", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item_type} - {self.itinerary}"

class Itinerary(models.Model):
    user = models.ForeignKey(Account, related_name="itineraries", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
