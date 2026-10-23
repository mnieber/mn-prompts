from django.urls import path
from blogs_be.users.views.sign_up_user_api_view import SignUpUserApiView
from blogs_be.users.views.sign_in_user_api_view import SignInUserApiView
from blogs_be.users.views.user_id_api_view import UserIdApiView
from blogs_be.users.views.refresh_token_api_view import RefreshTokenApiView

urlpatterns = [
    path("sign-up/", SignUpUserApiView.as_view(), name="sign-up-user"),
    path("sign-in/", SignInUserApiView.as_view(), name="sign-in-user"),
    path("user-id/", UserIdApiView.as_view(), name="user-id"),
    path("refresh-token/", RefreshTokenApiView.as_view(), name="refresh-token"),
]
