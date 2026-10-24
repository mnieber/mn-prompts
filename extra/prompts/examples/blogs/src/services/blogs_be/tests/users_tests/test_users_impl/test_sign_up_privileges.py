from users_tests.users_test_env import PASSWORD, Context, TestEnv

from django.contrib.auth import get_user_model

MALLORY = "mallory@example.com"


def create_env(context: Context):
    return Env(context)


def test_sign_up_privileges(context: Context):
    # Create the test environment
    env = create_env(context)

    # Mallory signs up, and asks to become a staff member and a superuser.
    #
    # Her account should be created, but these privileges should be ignored.
    if env.step(
        env.sign_up_with_extra_fields(MALLORY, is_staff=True, is_superuser=True),
    ):
        assert env.response.status_code == 201
        assert env.user_privileges(MALLORY) == {
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }


class Env(TestEnv):
    def sign_up_with_extra_fields(self, email: str, **extra_fields):
        self._post(
            "sign-up-user",
            create_user_form=dict(
                email=email,
                password=PASSWORD,
                password_confirmation=PASSWORD,
                **extra_fields,
            ),
        )

    # Queries

    def user_privileges(self, email: str):
        user = get_user_model().objects.get(email=email)
        return dict(
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
