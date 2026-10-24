import typing as T

import django.contrib.auth.models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from blogs_be.common.models import BaseModel
from blogs_be.users.actions.create_user import CreateUserForm
from django.db import models


class UserManager(django.contrib.auth.models.UserManager):
    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        from blogs_be.users.actions.create_user import create_user

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return create_user(
            CreateUserForm(
                email=email,
                password=password,
                password_confirmation=password,
            ),
            is_staff=extra_fields["is_staff"],
            is_superuser=extra_fields["is_superuser"],
            is_active=extra_fields["is_active"],
        )

    def active_with_confirmed_email(self):
        return self.filter(email_activated=True, is_active=True)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: T.List[str] = []

    email = models.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True,
        error_messages={"unique": _("User with this email already exists.")},
    )
    is_email_activated = models.BooleanField(default=False)
    firstname = models.CharField(max_length=255, default="anonymous")
    lastname = models.CharField(max_length=255, default="anonymous")
    is_active = models.BooleanField("active", default=False)
    is_anonymous = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField("date joined", auto_now_add=True)
    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default="unknown",
    )

    @property
    def fullname(self):
        return self.firstname + " " + self.lastname

    def _delete(self, using=None):
        super().delete(using=using)

    def delete(self, using=None):
        from blogs_be.users.actions.delete_user import delete_user

        delete_user(self, using=using)


class BlockedToken(BaseModel):
    jti = models.TextField(unique=True)
