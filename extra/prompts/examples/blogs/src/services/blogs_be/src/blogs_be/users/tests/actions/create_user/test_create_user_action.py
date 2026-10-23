import pytest
from django.contrib.auth import get_user_model

from blogs_be.users.actions.create_user import (
    CreateUserForm,
    PasswordsDoNotMatchError,
    UserWithEmailAlreadyExistsError,
    create_user,
)
from blogs_be.users.tests.factories import UserFactory

User = get_user_model()


class TestCreateUserAction:
    @pytest.mark.django_db
    def test_create_user_success(self):
        # Given
        create_user_form = CreateUserForm(
            email="newuser@example.com",
            password="password123",
            password_confirmation="password123",
        )

        # When
        user = create_user(create_user_form)

        # Then
        assert user.email == "newuser@example.com"
        assert user.check_password("password123")
        assert not user.is_active

    @pytest.mark.django_db
    def test_create_user_email_already_exists(self):
        # Given
        existing_user = UserFactory(email="existing@example.com")
        create_user_form = CreateUserForm(
            email="existing@example.com",
            password="password123",
            password_confirmation="password123",
        )

        # When / Then
        with pytest.raises(UserWithEmailAlreadyExistsError):
            create_user(create_user_form)

    @pytest.mark.django_db
    def test_create_user_passwords_do_not_match(self):
        # Given
        create_user_form = CreateUserForm(
            email="newuser@example.com",
            password="password123",
            password_confirmation="password456",
        )

        # When / Then
        with pytest.raises(PasswordsDoNotMatchError):
            create_user(create_user_form)
