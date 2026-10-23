from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory
from django.core.management.base import BaseCommand

from django.core.management import call_command
from blogs_be.users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-migrations",
            action="store_true",
            help="Delete all migration files",
        )

    def handle(self, reset_migrations=False, **options):
        if reset_migrations:
            call_command("delete-migration-files")
            call_command("makemigrations")

        call_command("reset_db")
        call_command("migrate")
        call_command("createsuperuser", "--noinput")

        user = User.objects.all().first()

        blog = BlogFactory(owner=user, name="Music")
        BlogPostFactory(blog=blog, title="Jazz", content="Jazz 1-2-3")
        BlogPostFactory(blog=blog, title="Pop", content="Pop 1-2-3")
        BlogPostFactory(blog=blog, title="Rock", content="Pop 1-2-3")

        blog = BlogFactory(owner=user, name="Movies")
        BlogPostFactory(blog=blog, title="Bambi", content="Disney")
        BlogPostFactory(blog=blog, title="Rocky", content="Boxing")
