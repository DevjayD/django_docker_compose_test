# python imports

# django imports
from django.urls import path, include

# third-party imports

# inter-app imports

# local imports

# app name
app_name = "accounts"

urlpatterns = [
    path("api/", include("accounts.api.urls")),  # apis
]
