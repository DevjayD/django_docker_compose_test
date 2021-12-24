import json
from datetime import datetime

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from accounts.messages import SYSTEM_SUCCESS_MESSAGE
from accounts.permissions import IsSuperUserOrReadOnly
from restaurant.api.v1.serializers import (
    CompanyModelSerializer,
    MenuModelSerializer,
    RestaurantModelSerializer,
    VotingSerializer,
)
from restaurant.models import Company, Menu, Restaurant, Voting


class CompanyModelViewSet(viewsets.ModelViewSet):
    """
    BASEURL : /restaurant/api/v1/company


        Create:
        Method: post
            url = BASEURL
            data:
                {
                    "id": 3,
                    "name": "CompanyThree",
                    "mobile_number": "+919977661166",
                    "email": null,
                    "last_updated": "2021-08-19T04:45:33.127767Z",
                    "timestamp": "2021-08-19T04:45:33.127804Z"
                }


        Retrieve:
            Method: get
            url = BASEURL
            example : BASEURL/id
            response :
                {
                    "id": 3,
                    "name": "CompanyThree",
                    "mobile_number": "+919977661166",
                    "email": null,
                    "last_updated": "2021-08-19T04:45:33.127767Z",
                    "timestamp": "2021-08-19T04:45:33.127804Z"
                }

        List:
            Method : get
            url = BASEURL
            exmaple : BASEURL

        Patch:
            Method : patch
            url = BASEURL
            example : BASEURL/id
            data:
                {
                    "name":"CompanyOneChangeToNewCompnay",
                    "mobile_number":"+919977661166"
                }
    """

    permission_classes = [IsAdminUser]
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer


class RestaurantModelViewSet(viewsets.ModelViewSet):
    """
    BASEURL : /restaurant/api/v1/restaurant
    Create:
        Method: post
        url = BASEURL
        data:
            {
                "id": 1,
                "name": "RestaurantOne",
                "mobile_number": "+919977557766",
                "email": null,
                "company": 1,
                "last_updated": "2021-08-18T12:10:47.858715Z",
                "timestamp": "2021-08-18T12:10:47.858742Z"
            }

    Retrieve:
        Method: get
        url = BASEURL
        example : BASEURL/id
        response :
            {
                "id": 3,
                "name": "RestaurantThree",
                "mobile_number": "+919977557766",
                "email": null,
                "company": 1,
                "last_updated": "2021-08-19T03:37:43.148665Z",
                "timestamp": "2021-08-19T03:37:43.148695Z"
            }

    List:
        Method : get
        url = BASEURL
        exmaple : BASEURL

    Patch:
        Method : patch
        url = BASEURL
        example : BASEURL/id
        data:
            {
                "name":"RestaurantChangesToFour"
            }
    """

    permission_classes = [IsAdminUser]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer


class MenuModelViewSet(viewsets.ModelViewSet):
    """
    BASEURL : /restaurant/api/v1/menu
    Create:
        Method: post
        url = BASEURL
        data:
            {
            'name': 'MenuEight',
            'mobile_number': '+919977661166',
            'restaurant': '1'
            'menu_file': <select_file>,

            }
    Retrieve:
        Method: get
        url = BASEURL
        example : BASEURL/id
        response :
            {
                "id": 8,
                "name": "MenuEight",
                "restaurant": 1,
                "menu": "{\n    \"Item_1\": \"this is item 1\",",
                "votes": 1,
                "last_updated": "2021-08-19T04:28:24.492841Z",
                "timestamp": "2021-08-19T04:28:24.492880Z"
            }

    List:
        Method : get
        url = BASEURL
        exmaple : BASEURL

    Patch:
        Method : patch
        url = BASEURL
        example : BASEURL/id
        data:
            {
                "name":"MenuOneToMenuNine"
            }
    List:
        Method : get
        url = BASEURL
        example : BASEURL/?todays_result=True
        accepted params:
            todays_result : True/False
            restaurant_id : <id>

    """

    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = MenuModelSerializer
    queryset = Menu.objects.all()

    def get_queryset(self) -> list:
        queryset = super(MenuModelViewSet, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset

        queryset = queryset.filter(timestamp__date=datetime.now().date())

        if self.request.GET.get("restaurant_id"):
            restaurant_id = self.request.GET.get("restaurant_id")
            queryset = queryset.filter(restaurant_id=restaurant_id)

        if self.request.GET.get("todays_result"):
            queryset = queryset.filter(menu_votes__votes__gt=0).order_by(
                "menu_votes__-votes"
            )

        return queryset


class VotingGenericView(GenericAPIView):
    """
    Create:
        Method: post
        url = BASEURL
        data:
            {
                'menu_id': 8
            }
    """

    permission_classes = [IsAuthenticated]
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer

    def post(self, request, *args, **kwargs) -> json:
        serializer_class = VotingSerializer(
            data=request.data, context={"request": request}
        )
        if serializer_class.is_valid(raise_exception=True):
            return Response(
                data={
                    "status": SYSTEM_SUCCESS_MESSAGE["VOTING_SUCCESSFUL"]
                },
                status=HTTP_200_OK,
            )
        return Response(
            serializer_class.errors, status=HTTP_400_BAD_REQUEST
        )
