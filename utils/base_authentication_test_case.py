from django.test.client import Client
from rest_framework.test import APITestCase


class BaseAuthenticatedTestCase(APITestCase):
    def setUp(self) -> None:
        self.client.login(
            username="thechip911@gmail.com", password="aloksharma"
        )
        # Employee Client Login
        self.employee_user_client = Client()
        self.employee_user_client.login(
            username="thechip3@gmail.com", password="aloksharma"
        )

        # SuperUser Client Login
        self.superuser_client = Client()
        self.superuser_client.login(
            username="thechip911@gmail.com", password="aloksharma"
        )
        super(BaseAuthenticatedTestCase, self).setUp()
