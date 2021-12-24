# python imports

# django imports
from django.urls import path

# third party imports
from rest_framework import routers

# local imports
# from .views import ()
from accounts.api.v1.views import LoginGenericView, EmployeeModelViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(
    r"employee", EmployeeModelViewSet, basename="employee"
)  # Employee CRUD

urlpatterns = [
    path(
        "login", LoginGenericView.as_view(), name="login"
    ),  # User Login URL
]

urlpatterns += router.urls
