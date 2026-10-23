import copy

from dataclassy import dataclass
from django.contrib.auth import get_user_model
import typing as T


@dataclass
class CreateUserForm:
    email: str
    password: str
    password_confirmation: str
    is_staff: T.Optional[bool] = False
    is_superuser: T.Optional[bool] = False
    is_active: T.Optional[bool] = False


def create_user(create_user_form: CreateUserForm):
    User = get_user_model()

    create_user_form = copy.deepcopy(create_user_form)
    create_user_form.email = User.objects.normalize_email(create_user_form.email)
    _validate_args(create_user_form)

    user = User(
        email=create_user_form.email,
        is_staff=create_user_form.is_staff,
        is_superuser=create_user_form.is_superuser,
        is_active=create_user_form.is_active,
    )

    if not create_user_form.password:
        user.set_unusable_password()
    else:
        user.set_password(create_user_form.password)

    user.save()

    return user


def _validate_args(create_user_form: CreateUserForm):
    User = get_user_model()

    if User.objects.filter(email=create_user_form.email).exists():
        raise UserWithEmailAlreadyExistsError()

    if create_user_form.password != create_user_form.password_confirmation:
        raise PasswordsDoNotMatchError()


class UserWithEmailAlreadyExistsError(Exception):
    pass


class PasswordsDoNotMatchError(Exception):
    pass
