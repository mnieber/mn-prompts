from users_tests.users_test_env import Context, TestEnv

ALICE = "alice@example.com"


def create_env(context: Context):
    return Env(context)


def test_a_user_signs_up_and_signs_in(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up.
    #
    # Her account should be created, and it should be active.
    if env.step(
        env.sign_up(ALICE),
    ):
        assert env.response.status_code == 201
        assert env.response_json() == {
            "id": env.user_ids[ALICE],
            "email": ALICE,
            "is_active": True,
        }

    # Alice signs in.
    #
    # She should receive an access token and a refresh token.
    if env.step(
        env.sign_in(ALICE),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["access_token"]
        assert env.response_json()["refresh_token"]

    # The frontend asks who is signed in.
    #
    # It should be Alice.
    if env.step(
        env.get_user_id(),
    ):
        assert env.response_json() == {"user_id": ALICE}


class Env(TestEnv):
    def get_user_id(self):
        self._get("user-id")
