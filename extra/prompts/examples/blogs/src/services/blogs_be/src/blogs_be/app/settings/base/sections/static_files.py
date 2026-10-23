import os

from .paths import APP_DIR, BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Strange enough, without adding the static dir to STATICFILES_DIRS Django won't
# use this directory, even though "app" is in INSTALLED_APPS.
STATICFILES_DIRS = [os.path.join(APP_DIR, "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
