import pytest
from django.contrib.auth import get_user_model

from blogs_be.users.actions.sign_in_user import (
    InvalidCredentialsError,
    SignInUserForm,
    sign_in_user,
)
from blogs_be.users.tests.factories import InactiveUserFactory, UserFactory
from blogs_be.users.actions.sign_in_user import AccountIsNotActiveError

User = get_user_model()


class TestSignInUserAction:
    @pytest.mark.django_db
    def test_sign_in_user_action_success(self):
        # Given
        user = UserFactory(email="user@example.com")
        user.set_password("password123")
        user.save()

        sign_in_user_form = SignInUserForm(
            email="user@example.com",
            password="password123",
        )

        # When
        tokens = sign_in_user(sign_in_user_form)

        # Then
        assert tokens.get("access_token")
        assert tokens.get("refresh_token")

    @pytest.mark.django_db
    def test_sign_in_user_action_invalid_credentials(self):
        # Given
        UserFactory(email="user@example.com")
        sign_in_user_form = SignInUserForm(
            email="user@example.com",
            password="wrongpassword",
        )

        # When / Then
        with pytest.raises(InvalidCredentialsError):
            sign_in_user(sign_in_user_form)

    @pytest.mark.django_db
    def test_sign_in_user_action_inactive_user(self):
        # Given
        user = InactiveUserFactory(email="inactive@example.com")
        user.set_password("password123")
        user.save()

        sign_in_user_form = SignInUserForm(
            email="inactive@example.com",
            password="password123",
        )

        # When / Then
        with pytest.raises(AccountIsNotActiveError):
            sign_in_user(sign_in_user_form)
