from blogs_be.app.utils.env import env

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DJANGO_DATABASE_NAME"),
        "USER": env("DJANGO_DATABASE_USER"),
        "PASSWORD": env("DJANGO_DATABASE_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    },
}

MIGRATION_MODULES = {}

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "/app/dumps"}
