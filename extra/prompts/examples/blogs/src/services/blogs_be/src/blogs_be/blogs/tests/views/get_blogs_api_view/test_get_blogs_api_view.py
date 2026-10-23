# blogs/tests/views/test_get_blogs_api_view.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blogs_be.blogs.tests.factories import BlogFactory
from blogs_be.users.tests.factories import UserFactory


class TestGetBlogsApiView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.mark.django_db
    def test_get_blogs_view_success(self, api_client, user):
        # Given
        owner1 = UserFactory()
        owner2 = UserFactory()
        BlogFactory.create_batch(2, owner=owner1)
        BlogFactory(owner=owner2)
        url = reverse("get-blogs")

        # When
        response = api_client.get(url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert set(str(blog["owner_id"]) for blog in response.data) == {
            str(owner1.id),
            str(owner2.id),
        }
