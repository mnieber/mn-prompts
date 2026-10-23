from blogs_be.app.settings.local.inherit import CACHES

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
}
