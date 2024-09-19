from django.urls import path
from . import views

urlpatterns = [
    # Trip endpoints
    path("", views.TripListView.as_view(), name="trip_list"),
    path("<int:pk>/", views.TripDetailView.as_view(), name="trip_detail"),

    # Itinerary endpoints
    path('itineraries/', views.ItineraryListCreateView.as_view(), name='itinerary-list-create'),
    path('itineraries/<int:pk>/', views.ItineraryDetailView.as_view(), name='itinerary-detail'),

    # Itinerary Item endpoints
    path('itinerary-items/<int:pk>/', views.ItineraryItemDetailView.as_view(), name='itinerary-item-detail'),
    path('<int:itinerary_pk>/itinerary-items/', views.ItineraryItemListCreateView.as_view(), name='itinerary-item-list-create'),
]
