# python imports

# django imports

# third party imports
from django.urls import path
from rest_framework import routers

# local imports
from restaurant.api.v1.views import (
    CompanyModelViewSet,
    MenuModelViewSet,
    RestaurantModelViewSet,
    VotingGenericView,
)

router = routers.SimpleRouter(trailing_slash=False)

router.register(
    r"company", CompanyModelViewSet, basename="company"
)  # Company URL
router.register(
    r"restaurant", RestaurantModelViewSet, basename="restaurant"
)  # Restaurant URL
router.register(r"menu", MenuModelViewSet, basename="menu")  # Menu URL

urlpatterns = [
    path(
        "voting", VotingGenericView.as_view(), name="voting"
    ),  # Voting API
]

urlpatterns += router.urls
