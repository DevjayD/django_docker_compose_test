# python imports

# django imports
from django.urls import path, include

# third-party imports

# inter-app imports

# local imports


urlpatterns = [
    path("v1/", include("restaurant.api.v1.urls")),
    path("v2/", include("restaurant.api.v2.urls")),
]
