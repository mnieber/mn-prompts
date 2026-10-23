from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


def get_user_or_400(user_id):
    user = User.objects.filter(pk=user_id).first()
    if not user:
        raise ValidationError(code="USER_NOT_FOUND")
    return user
