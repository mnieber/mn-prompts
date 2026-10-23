import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from blogs_be.users.tests.factories import InactiveUserFactory, UserFactory
from blogs_be.common.utils.test_utils import has_error_code


class TestSignInUserApiView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_sign_in_user_api_view_success(self, api_client):
        # Given
        user = UserFactory(email="user@example.com")
        user.set_password("password123")
        user.save()

        url = reverse("sign-in-user")
        data = {
            "sign_in_user_form": {
                "email": "user@example.com",
                "password": "password123",
            }
        }

        # When
        response = api_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("access_token")
        assert response.data.get("refresh_token")

    @pytest.mark.django_db
    def test_sign_in_user_api_view_invalid_credentials(self, api_client):
        # Given
        UserFactory(email="user@example.com")
        url = reverse("sign-in-user")
        data = {
            "sign_in_user_form": {
                "email": "user@example.com",
                "password": "wrongpassword",
            }
        }

        # When
        response = api_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert has_error_code(response, "INVALID_CREDENTIALS")

    @pytest.mark.django_db
    def test_sign_in_user_api_view_inactive_user(self, api_client):
        # Given
        user = InactiveUserFactory(email="inactive@example.com")
        user.set_password("password123")
        user.save()

        url = reverse("sign-in-user")
        data = {
            "sign_in_user_form": {
                "email": "inactive@example.com",
                "password": "password123",
            }
        }

        # When
        response = api_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert has_error_code(response, "INACTIVE_ACCOUNT")
