from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Trip)
admin.site.register(models.Itinerary)
admin.site.register(models.ItineraryItem)
admin.site.register(models.Activity)