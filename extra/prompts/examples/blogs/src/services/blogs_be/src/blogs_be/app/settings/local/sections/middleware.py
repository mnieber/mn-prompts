from blogs_be.app.settings.local.inherit import MIDDLEWARE

# This logs request bodies, including passwords, so it must stay out of the base settings.
MIDDLEWARE += [
    "blogs_be.app.middleware.request_logging.request_logging_middleware",
]
