# Inner APP Import
# Django Imports
from django.contrib.auth import get_user_model
from django.urls import reverse

# Rest FrameWork Import
from rest_framework import status
from rest_framework.test import APITestCase

from utils.base_authentication_test_case import BaseAuthenticatedTestCase

# Import User Model
User = get_user_model()


class EmployeeTests(BaseAuthenticatedTestCase):
    fixtures = ["data.json"]

    def test_create_employee(self):
        """
        Ensure we can create a new Employee object
        and Get an error on creating Employee with same Email
        """
        data = {
            "name": "TestCaseName",
            "email": "testcaseemail@gmail.com",
            "password": "testcase",
        }

        response = self.superuser_client.post(
            reverse("accounts:employee-list"), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_for_duplicate = self.client.post(
            reverse("accounts:employee-list"), data=data
        )
        self.assertEqual(
            response_for_duplicate.status_code, status.HTTP_400_BAD_REQUEST
        )

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.post(
            reverse("accounts:employee-list"), data=data
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_create_employee_bad_email(self):
        """
        Ensure that if we can create an employee with bad email format
        """
        data = {
            "name": "TestCaseName",
            "email": "testcaseemailgmail.com",
            "password": "testcase",
        }

        response = self.superuser_client.post(
            reverse("accounts:employee-list"), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.post(
            reverse("accounts:employee-list"), data=data
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_employee_edit(self):
        # import ipdb; ipdb.set_trace()
        """
        For Editing the Employee
        """
        data = {"name": "TestEmployee Name"}
        response = self.superuser_client.patch(
            reverse("accounts:employee-detail", args=[2]),
            data=data,
            content_type="application/json",
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], data["name"])

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.patch(
            reverse("accounts:employee-detail", args=[2]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_employee_delete(self):
        """
        For Deleting the Company
        """
        response = self.superuser_client.delete(
            reverse("accounts:employee-detail", args=[2])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.delete(
            reverse("accounts:employee-detail", args=[2])
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_get_users_list(self):
        """
        Ensure that we are Getting the Employee list that are in our database
        """
        users = User.objects.filter(is_employee=True)
        response = self.superuser_client.get(
            reverse("accounts:employee-list")
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), users.count())

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.get(
            reverse("accounts:employee-list")
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )


class LoginTests(APITestCase):
    fixtures = ["data.json"]

    def test_login_success(self):
        """
        Ensure that we are getting logged in Successfully
        """
        data = {"email": "thechip1@gmail.com", "password": "aloksharma"}

        response = self.client.post(reverse("accounts:login"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        """
        Ensure that we are get forbidden error on wrong credentials
        """
        data = {"email": "thechip1@gmail.com", "password": "aloksharm"}

        response = self.client.post(reverse("accounts:login"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
