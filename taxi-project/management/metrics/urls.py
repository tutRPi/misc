from django.urls import path
from .views import RevenuePerCity, TripLength

app_name = "metrics"
urlpatterns = [

    path('revenue-per-city', RevenuePerCity.as_view(), name="revenue_per_city"),
    path('trip-length', TripLength.as_view(), name="trip_length"),
]
