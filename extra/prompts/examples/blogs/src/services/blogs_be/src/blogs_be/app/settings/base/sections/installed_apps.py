DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
]

THIRD_PARTY_APPS = [
    "adminsortable2",
    "dbbackup",
    "django_extensions",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "drf_standardized_errors",
    "allauth",
    "allauth.account",
    "allauth.headless",
]

LOCAL_APPS = [
    "blogs_be.api.apps.ApiConfig",
    "blogs_be.app.apps.AppConfig",
    "blogs_be.blogs.apps.BlogsConfig",
    "blogs_be.users.apps.UsersConfig",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
