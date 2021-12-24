# Django Imports
from django.urls import reverse

# RestFramework Imports
from rest_framework import status

# App Imports
from restaurant.models import Company, Restaurant, Menu
from restaurant_manager.settings import TEST_CSV_FILE_PATH

# Inner APP Imports
from utils.base_authentication_test_case import BaseAuthenticatedTestCase


class CompanyTests(BaseAuthenticatedTestCase):
    fixtures = ["data.json"]

    def test_company_create(self):
        """
        Ensure we can create a new Company object.
        """
        data = {
            "name": "CompanyNameForTest Case",
            "mobile_number": "+919999776677",
        }

        response = self.superuser_client.post(
            reverse("restaurant:company-list"), data=data
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], data["name"])
        self.assertEqual(
            json_response["mobile_number"], data["mobile_number"]
        )

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.post(
            reverse("restaurant:company-list"), data=data
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

        # For Checking That we are Getting Error
        # on Creating a company with same name
        data_with_same_name = {
            "name": "CompanyNameForTest Case",
            "mobile_number": "+919999776691",
        }
        response_for_duplicate_company = self.superuser_client.post(
            reverse("restaurant:company-list"), data=data_with_same_name
        )
        self.assertEqual(
            response_for_duplicate_company.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_company_edit(self):
        """
        For Editing the Company
        """
        data = {
            "name": "CompanyNameForTest Case",
            "mobile_number": "+919999776677",
        }
        response = self.superuser_client.patch(
            reverse("restaurant:company-detail", args=[2]),
            data=data,
            content_type="application/json",
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], data["name"])
        self.assertEqual(
            json_response["mobile_number"], data["mobile_number"]
        )

    def test_company_delete(self):
        """
        For Deleting the Company
        """
        response = self.superuser_client.delete(
            reverse("restaurant:company-detail", args=[2])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.delete(
            reverse("restaurant:company-detail", args=[2])
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_company_list(self):
        """
        For List of the Company
        """
        company = Company.objects.all()
        response = self.superuser_client.get(
            reverse("restaurant:company-list")
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), company.count())

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.get(
            reverse("restaurant:company-list")
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )


class RestaurantTests(BaseAuthenticatedTestCase):
    fixtures = ["data.json"]

    def test_restaurant_create(self):
        """
        Ensure we can create a new Restaurant object.
        """
        data = {
            "name": "RestaurantNameForTest Case",
            "mobile_number": "+919999776677",
            "company": 1,
        }

        response = self.superuser_client.post(
            reverse("restaurant:restaurant-list"), data=data
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], data["name"])
        self.assertEqual(
            json_response["mobile_number"], data["mobile_number"]
        )

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.post(
            reverse("restaurant:restaurant-list"), data=data
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

        # For Checking That we are Getting Error on
        # Creating a Restaurant with same name
        data_with_same_name = {
            "name": "RestaurantNameForTest Case",
            "mobile_number": "+919999776691",
            "company": 1,
        }
        response_for_duplicate_restaurant = self.superuser_client.post(
            reverse("restaurant:restaurant-list"), data=data_with_same_name
        )
        self.assertEqual(
            response_for_duplicate_restaurant.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_restaurant_edit(self):
        """
        For Editing the Restaurant
        """
        data = {
            "name": "RestaurantNameForTest Case",
            "mobile_number": "+919999776677",
        }
        response = self.superuser_client.patch(
            reverse("restaurant:restaurant-detail", args=[2]),
            data=data,
            content_type="application/json",
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], data["name"])
        self.assertEqual(
            json_response["mobile_number"], data["mobile_number"]
        )

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.patch(
            reverse("restaurant:restaurant-detail", args=[2]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_restaurant_delete(self):
        """
        For Deleting the Restaurant
        """
        response = self.superuser_client.delete(
            reverse("restaurant:restaurant-detail", args=[2])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.delete(
            reverse("restaurant:restaurant-detail", args=[2])
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_restaurant_list(self):
        """
        For List of the Restaurant
        """
        company = Restaurant.objects.all()
        response = self.superuser_client.get(
            reverse("restaurant:restaurant-list")
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), company.count())

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.get(
            reverse("restaurant:restaurant-list")
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )


class MenuTests(BaseAuthenticatedTestCase):
    fixtures = ["data.json"]

    def test_menu_create(self):
        """
        Ensure we can create a new Menu object.
        """
        data = {"name": "MenuTwelve", "restaurant": 1}
        with open(TEST_CSV_FILE_PATH, "r") as f:
            data["menu_file"] = f

            response = self.superuser_client.post(
                reverse("restaurant:menu-list"), data=data
            )
            json_response = response.json()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(json_response["name"], data["name"])
            self.assertIsNotNone(json_response["menu"])

            # For Testing if Employee is authorised or not
            response_for_employee = self.employee_user_client.post(
                reverse("restaurant:menu-list"), data=data
            )
            self.assertEqual(
                response_for_employee.status_code,
                status.HTTP_403_FORBIDDEN,
            )

    def test_menu_edit(self):
        """
        For Editing the Menu
        """
        # content_type="multipart/form-data;boundary=SOME_BOUNDARY,application/json"
        data = {"name": "MenuNameForTest Case"}
        with open(TEST_CSV_FILE_PATH, "r") as f:
            data["menu_file"] = f
            response = self.client.patch(
                reverse("restaurant:menu-detail", args=[2]), data=data
            )
            json_response = response.json()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(json_response["name"], data["name"])
            self.assertIsNotNone(json_response["menu"])

    def test_menu_delete(self):
        """
        For Deleting the Menu
        """
        response = self.superuser_client.delete(
            reverse("restaurant:menu-detail", args=[2])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # For Testing if Employee is authorised or not
        response_for_employee = self.employee_user_client.delete(
            reverse("restaurant:menu-detail", args=[2])
        )
        self.assertEqual(
            response_for_employee.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_menu_list(self):
        """
        For List of the Menu
        """
        menu = Menu.objects.all()
        response = self.superuser_client.get(
            reverse("restaurant:menu-list")
        )
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), menu.count())


class VotingTests(BaseAuthenticatedTestCase):
    fixtures = ["data.json"]

    def test_for_voting(self):
        """
        Ensure we can Vote
        """
        data = {"menu_id": 8}

        response = self.employee_user_client.post(
            reverse("restaurant:voting"), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_for_duplicate_vote = self.employee_user_client.post(
            reverse("restaurant:voting"), data=data
        )
        self.assertEqual(
            response_for_duplicate_vote.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
