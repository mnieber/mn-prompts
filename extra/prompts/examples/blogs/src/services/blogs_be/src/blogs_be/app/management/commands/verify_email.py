from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand, CommandError

from blogs_be.users.models import User


class Command(BaseCommand):
    help = "Mark the email address of a user as verified, so that they can sign in"

    def add_arguments(self, parser):
        parser.add_argument("email", help="The email address of the user")

    def handle(self, email, **options):
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            raise CommandError(f"There is no user with email {email}")

        email_address, _ = EmailAddress.objects.update_or_create(
            user=user,
            email__iexact=user.email,
            defaults=dict(email=user.email, verified=True),
            create_defaults=dict(email=user.email, verified=True, primary=True),
        )
        if not EmailAddress.objects.filter(user=user, primary=True).exists():
            email_address.primary = True
            email_address.save(update_fields=["primary"])

        self.stdout.write(f"Verified the email address of {user.email}")
