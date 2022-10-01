from django.urls import path
from . import views
from .views import RevenuePerCity

app_name = "metrics"
urlpatterns = [

    path('revenue-per-city', RevenuePerCity.as_view(), name="revenue_per_city"),
]
