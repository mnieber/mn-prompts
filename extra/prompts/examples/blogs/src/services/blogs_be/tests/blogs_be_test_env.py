import typing as T

from allauth.account.models import EmailAddress
from django.urls import reverse
from rest_framework.test import APIClient

from blogs_be.common.utils.dataclass import dataclass
from blogs_be.users.tests.factories import UserFactory

PASSWORD = "correct horse battery staple"

AUTH_URL = "/api/_allauth/browser/v1/auth/"


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

    def sign_up(self, email: str, password=PASSWORD):
        self._post_auth("signup", email=email, password=password)

    def sign_in(self, email: str, password=PASSWORD):
        """Signs in, and uses the session cookie in the next requests."""
        self._post_auth("login", email=email, password=password)

    def sign_up_and_sign_in(self, email: str):
        """Creates the account directly, so that these tests don't depend on the emails."""
        self.sign_out()
        user = UserFactory(email=email, password=PASSWORD)
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        self.user_ids[email] = str(user.id)
        self.sign_in(email)

    def sign_out(self):
        self.response = self.context.api_client.delete(f"{AUTH_URL}session")

    def _post(self, url_name: str, url_kwargs=None, **data):
        self.response = self.context.api_client.post(
            reverse(url_name, kwargs=url_kwargs), data, format="json"
        )

    def _post_auth(self, path: str, **data):
        self.response = self.context.api_client.post(
            f"{AUTH_URL}{path}", data, format="json"
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

    def error_details(self) -> T.List[str]:
        return [error["detail"] for error in self.response.json()["errors"]]
