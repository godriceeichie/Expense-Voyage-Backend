from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Trip)
admin.site.register(models.Itinerary)
admin.site.register(models.ItineraryItem)
admin.site.register(models.Activity)
admin.site.register(models.Destination)

@admin.register(models.Trip)
class AccountAdmin(admin.ModelAdmin):
    # list_display = ["email", "name", "created_at"]
    # list_filter=["created_at"]
    search_fields = ["trip_name", "destination"]