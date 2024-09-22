from rest_framework import generics, permissions,response, status
from  . import models,serializers
from django.shortcuts import get_object_or_404

# Create your views here.
class TripListView(generics.ListCreateAPIView):
    queryset = models.Trip.objects.all()
    serializer_class = serializers.TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        trip_serializer = self.get_serializer_class()
        trip = trip_serializer(data=self.request.data)
        trip.is_valid()
        trip.save(user=user)

        return response.Response(trip.data)

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Trip.objects.all()
    serializer_class = serializers.TripSerializer
    permission_classes = [permissions.IsAuthenticated]
        
class ItineraryListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch only itineraries for the logged-in user
        return models.Itinerary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the itinerary with the logged-in user
        serializer.save(user=self.request.user)

# Retrieve/Update/Delete Itinerary
class ItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch only itineraries belonging to the logged-in user
        return models.Itinerary.objects.filter(user=self.request.user)
    
# List/Create Itinerary Items
class ItineraryItemListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ItineraryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch only items for itineraries of the logged-in user
        return models.ItineraryItem.objects.filter(itinerary__user=self.request.user)

    def perform_create(self, serializer):
        # Ensure item is attached to a user's itinerary
        itinerary_pk = self.kwargs["itinerary_pk"]
        request_body = self.request.data

        itinerary = get_object_or_404(models.Itinerary, pk=itinerary_pk)
        # Variables for related fields
        lodge = None
        transport = None
        activity = None

        match request_body["item_type"]:
            case "lodge":
                lodge = models.Lodge.objects.create(
                    location=request_body.get("location"), 
                    address=request_body.get("address")
                )
                lodge.save()
            case "transport":
                transport  = models.Transport.objects.create(
                    transport_type = request_body.get("transport_type"),
                    departure_location = request_body.get("departure_location"),
                    arrival_location = request_body.get("arrival_location"),
                    departure_time = request_body.get("departure_time"),
                    arrival_time = request_body.get("arrival_time")
                )
                transport.save()
            case "activity":
                activity = models.Activity.objects.create(
                    timestamp = request_body.get("timestamp"),
                    location = request_body.get("location"),
                    activity_name = request_body.get("activity_name"),
                    activity_description = request_body.get("activity_description")
                )
                activity.save()

        # Save the ItineraryItem with the created Lodge/Transport/Activity
        serializer.save(itinerary=itinerary, lodge=lodge, transport=transport, activity=activity)

# Retrieve/Update/Delete Itinerary Item
class ItineraryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ItineraryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch only items for itineraries of the logged-in user
        return models.ItineraryItem.objects.filter(itinerary__user=self.request.user)
    
    def perform_update(self, serializer):
        itinerary_item = self.get_object()
        itinerary_item_serializer = self.get_serializer_class()
        serializer_class = itinerary_item_serializer(self.get_object())
        request_body = self.request.data.copy()
        print(serializer_class.data)

        lodge = itinerary_item.lodge
        transport = itinerary_item.transport
        activity = itinerary_item.activity

        match request_body["item_type"]:
            
            case "lodge":
                request_body.pop("item_type", None)
                if serializer_class.data["transport"] == None:
                    lodge = models.Lodge.objects.create(
                        location=request_body.get("location"), 
                        address=request_body.get("address")
                    )
                    lodge.save()
                    serializer.save(lodge=lodge)
                else:
                    lodge = models.Lodge.objects.filter(pk=serializer_class.data["lodge"]["id"]).update(**request_body)
                
            case "transport":
                request_body.pop("item_type", None)
                if serializer_class.data["transport"] == None:
                    transport = models.Transport.objects.create(
                        transport_type = request_body.get("transport_type"),
                        departure_location = request_body.get("departure_location"),
                        arrival_location = request_body.get("arrival_location"),
                        departure_time = request_body.get("departure_time"),
                        arrival_time = request_body.get("arrival_time")
                    )
                    transport.save()
                    serializer.save(transport=transport)
                else:
                    transport = models.Transport.objects.filter(pk=serializer_class.data["transport"]["id"]).update(**request_body)
                
            case "activity":
                request_body.pop("item_type", None)
                if serializer_class.data["activity"] == None:
                    activity = models.Activity.objects.create(
                        timestamp = request_body.get("timestamp"),
                        location = request_body.get("location"),
                        activity_name = request_body.get("activity_name"),
                        activity_description = request_body.get("activity_description")
                    )
                    activity.save()
                    serializer.save(activity=activity)
                else:
                   activity = models.Activity.objects.filter(pk=serializer_class.data["activity"]["id"]).update(**request_body) 
        
class CreateListDestinationView(generics.ListCreateAPIView):
    queryset = models.Destination.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.DestinationSerializer

    # def get(self, request, *args, **kwargs):
    #     # Check if user is an admin
    #     if not request.user.is_staff:
    #         return response.Response(
    #             {"detail": "You do not have permission to perform this action."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     return super().get(request, *args, **kwargs)