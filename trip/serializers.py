from rest_framework import serializers
from . import models

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = "__all__"
        read_only_fields = ("user",)


class LodgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lodge
        fields = ['id', 'location', 'address']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ['id', 'timestamp', 'location', 'activity_name', 'activity_description']

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transport
        fields = ['id', 'transport_type', 'departure_location', 'arrival_location', 'departure_time', 'arrival_time']

class ItineraryItemSerializer(serializers.ModelSerializer):
    lodge = LodgeSerializer(required=False)
    transport = TransportSerializer(required=False)
    activity = ActivitySerializer(required=False)

    class Meta:
        model = models.ItineraryItem
        fields = ['id', 'item_type', 'lodge', 'transport', 'activity']

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, required=False)

    class Meta:
        model = models.Itinerary
        fields = ['id', 'title', 'user', 'created_at', 'updated_at', 'items']
        read_only_fields = ['created_at', 'updated_at', 'user']