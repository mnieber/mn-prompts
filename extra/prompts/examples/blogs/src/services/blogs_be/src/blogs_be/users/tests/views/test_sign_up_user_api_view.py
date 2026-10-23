import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestSignUpUserApiView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_sign_up_user_api_view_success(self, api_client):
        # Given
        url = reverse("sign-up-user")
        data = {
            "create_user_form": {
                "email": "newuser@example.com",
                "password": "password123",
                "password_confirmation": "password123",
            }
        }

        # When
        response = api_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "newuser@example.com"
        assert response.data["is_active"] == True
