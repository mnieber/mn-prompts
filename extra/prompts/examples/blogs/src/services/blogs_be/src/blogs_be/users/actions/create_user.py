import copy

from dataclassy import dataclass
from django.contrib.auth import get_user_model


@dataclass
class CreateUserForm:
    email: str
    password: str
    password_confirmation: str


def create_user(
    create_user_form: CreateUserForm,
    is_staff: bool = False,
    is_superuser: bool = False,
    is_active: bool = False,
):
    User = get_user_model()

    create_user_form = copy.deepcopy(create_user_form)
    create_user_form.email = User.objects.normalize_email(create_user_form.email)
    _validate_args(create_user_form)

    user = User(
        email=create_user_form.email,
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
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
