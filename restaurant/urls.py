# python imports

# django imports
from django.urls import path, include

# third-party imports

# inter-app imports

# local imports

# app name
app_name = "restaurant"

urlpatterns = [
    path("api/", include("restaurant.api.urls")),
]
