import json

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from accounts.messages import SYSTEM_SUCCESS_MESSAGE
from restaurant.api.v2.serializers import VotingSerializer
from restaurant.models import Voting


class VotingGenericView(GenericAPIView):
    """
    BASEURL : /accounts/api/v1/create-employee
    Create:
        Method: post
        url = BASEURL
        data:
            {
                'menu_id': [1,2,3]
            }
    Retrieve:
        Method: get
        url = BASEURL
        example : BASEURL/id
        response:
            {
                "id": 8,
                "name": "TheChip",
                "email": "testemployee2@gmail.com"
            }
    Patch:
        Method : patch
        url = BASEURL
        example : BASEURL/id
        data:
            {
                "name":"TheChipChangedtoNewChip"
            }
    """

    permission_classes = [IsAuthenticated]
    queryset = Voting.objects.all()

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
