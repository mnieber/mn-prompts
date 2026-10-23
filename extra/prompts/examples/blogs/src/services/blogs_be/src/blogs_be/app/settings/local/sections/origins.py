from blogs_be.app.utils.get_internal_ips import get_internal_ips

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = get_internal_ips()
