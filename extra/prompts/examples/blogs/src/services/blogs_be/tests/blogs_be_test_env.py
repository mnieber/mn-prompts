import typing as T

from dataclassy import dataclass
from django.urls import reverse
from rest_framework.test import APIClient

PASSWORD = "correct horse battery staple"


@dataclass
class Context:
    api_client: APIClient


class TestEnv:
    __test__ = False

    def __init__(self, context: Context):
        self.context = context
        self.response = None
        self.user_ids: T.Dict[str, str] = {}

        self.__post_init__()

    def __post_init__(self):
        pass

    def step(self, *_):
        return True

    def sign_up(self, email: str, password=PASSWORD, password_confirmation=None):
        self._post(
            "sign-up-user",
            create_user_form=dict(
                email=email,
                password=password,
                password_confirmation=password_confirmation or password,
            ),
        )
        if self.response.status_code == 201:
            self.user_ids[email] = self.response.json()["id"]

    def sign_in(self, email: str, password=PASSWORD):
        """Signs in, and uses the access token in the next requests."""
        self._post(
            "sign-in-user", sign_in_user_form=dict(email=email, password=password)
        )
        if self.response.status_code == 200:
            access_token = self.response.json()["access_token"]
            self.context.api_client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {access_token}"
            )

    def sign_up_and_sign_in(self, email: str):
        self.sign_up(email)
        self.sign_in(email)

    def sign_out(self):
        """Stops sending the access token (as if the frontend forgets it)."""
        self.context.api_client.credentials()

    def _post(self, url_name: str, url_kwargs=None, **data):
        self.response = self.context.api_client.post(
            reverse(url_name, kwargs=url_kwargs), data, format="json"
        )

    def _get(self, url_name: str, url_kwargs=None):
        self.response = self.context.api_client.get(
            reverse(url_name, kwargs=url_kwargs)
        )

    # Queries

    def response_json(self):
        return self.response.json()

    def error_codes(self) -> T.List[str]:
        return [error["code"] for error in self.response.json()["errors"]]
