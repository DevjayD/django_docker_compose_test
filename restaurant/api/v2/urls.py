# python imports

# django imports
from django.urls import path

# third party imports
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
# from .views import ()
from restaurant.api.v2.views import VotingGenericView

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path(
        "voting", VotingGenericView.as_view(), name="voting"
    ),  # Voting API
]

urlpatterns += router.urls

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)
