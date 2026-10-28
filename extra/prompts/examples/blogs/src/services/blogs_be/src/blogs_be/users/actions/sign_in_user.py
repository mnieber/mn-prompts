from blogs_be.common.utils.dataclass import dataclass
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import rest_framework.exceptions

User = get_user_model()


@dataclass
class SignInUserForm:
    email: str
    password: str


def sign_in_user(sign_in_user_form: SignInUserForm):
    user = User.objects.filter(email=sign_in_user_form.email).first()
    if user and not user.is_active:
        raise AccountIsNotActiveError()

    serializer = TokenObtainPairSerializer(
        data={"email": sign_in_user_form.email, "password": sign_in_user_form.password}
    )

    try:
        serializer.is_valid(raise_exception=True)
    except rest_framework.exceptions.AuthenticationFailed:
        raise InvalidCredentialsError()

    if serializer.user and not serializer.user.is_anonymous:
        return dict(
            access_token=serializer.validated_data["access"],
            refresh_token=serializer.validated_data["refresh"],
        )
    else:
        raise InvalidCredentialsError()


class InvalidCredentialsError(Exception):
    pass


class AccountIsNotActiveError(Exception):
    pass
