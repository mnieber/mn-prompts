import deepdiff
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from blogs_be.common.utils.test_utils import DeepDiffOperator, rhs_is_not_none
from blogs_be.users.tests.factories import UserFactory


class TestCreateBlogApiView:
    @pytest.fixture()
    def api_client(self):
        api_client = APIClient()
        return api_client

    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.mark.django_db()
    def test_create_blog_api_view_success(self, api_client, blog_owner):
        # Given
        api_client.force_authenticate(user=blog_owner)
        url = reverse("create-blog")

        # When
        response = api_client.post(
            url,
            data=dict(
                create_blog_form=dict(
                    name="My blog",
                    description="My blog description",
                )
            ),
        )

        # Then
        assert response.status_code == 201

        result = response.json()
        diff = deepdiff.DeepDiff(
            {
                "id": "some id",
                "name": "My blog",
                "slug": "my-blog",
                "description": "My blog description",
                "owner_id": str(blog_owner.id),
                "audience": "any",
            },
            result,
            custom_operators=[
                DeepDiffOperator(rhs_is_not_none, "id"),
            ],
        )
        assert not diff, f"JSON response differs: {diff.pretty()}"
