from uuid import uuid4

from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from accounts.api.v1.serializers import UserLoginSerializer, UserSerializer
from accounts.messages import VALIDATION_ERROR_MESSAGES

User = get_user_model()


class LoginGenericView(generics.GenericAPIView):
    """
    BASEURL : /accounts/api/v1/login
    ```

        Create:
            Method: post
            url = BASEURL
            data:
               {
                    'email': 'thechip1@gmail.com',
                    'password': 'aloksharma'
                }
    ```
    """

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            password = serializer_class.validated_data.get("password")
            email = serializer_class.validated_data.get("email")
            authenticated_user = authenticate(
                username=email, password=password
            )
            if not authenticated_user:
                return Response(
                    data={
                        "status": VALIDATION_ERROR_MESSAGES[
                            "INVALID_CREDENTIALS"
                        ]
                    },
                    status=HTTP_403_FORBIDDEN,
                )
            else:
                token = uuid4()
                authenticated_user.token = token
                authenticated_user.save()
                serialized_data = UserSerializer(authenticated_user).data
                serialized_data.update({"token": token})
            return Response(data=serialized_data, status=HTTP_200_OK)
        return Response(
            serializer_class.errors, status=HTTP_400_BAD_REQUEST
        )


class EmployeeModelViewSet(viewsets.ModelViewSet):
    """
    ```
        BASEURL : /accounts/api/v1/create-employee
            Create:
            Method: post
            url = BASEURL
            data:
                {
                "name":"TheChip",
                "email":"testemployee1@gmail.com",
                "password":"aloksharma"
                }

            Retrieve:
            Method: get
            url = BASEURL
            example : BASEURL/id
            response :
                {
                    "id": 8,
                    "name": "TheChip",
                    "email": "testemployee2@gmail.com"
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
                    "name":"TheChiptoNewChip"
                }
    ```
    """

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_employee=True)
    permission_classes = [IsAdminUser]
