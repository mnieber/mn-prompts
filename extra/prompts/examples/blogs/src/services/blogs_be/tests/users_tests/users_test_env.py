import re
from urllib.parse import unquote

from blogs_be_test_env import AUTH_URL, PASSWORD, Context, TestEnv as BlogsBeTestEnv
from django.core import mail

__all__ = ["AUTH_URL", "PASSWORD", "Context", "TestEnv"]


class TestEnv(BlogsBeTestEnv):
    def verify_email(self):
        """Follows the link in the last email, like the frontend does."""
        self._post_auth("email/verify", key=self.emailed_key("account/verify-email"))

    def request_password_reset(self, email: str):
        self._post_auth("password/request", email=email)

    def reset_password(self, password: str):
        """Follows the link in the last email, like the frontend does."""
        self._post_auth(
            "password/reset",
            key=self.emailed_key("account/password/reset"),
            password=password,
        )

    def get_session(self):
        self.response = self.context.api_client.get(f"{AUTH_URL}session")

    # Queries

    def emailed_key(self, path: str) -> str:
        return unquote(re.search(rf"/{path}/(\S+)", mail.outbox[-1].body).group(1))

    def signed_in_email(self):
        self.get_session()
        if self.response.status_code != 200:
            return None
        return self.response.json()["data"]["user"]["email"]

    def pending_flows(self):
        flows = self.response.json()["data"]["flows"]
        return [flow["id"] for flow in flows if flow.get("is_pending")]
