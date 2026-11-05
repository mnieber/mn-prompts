from blogs_be.app.utils.get_internal_ips import get_internal_ips

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = get_internal_ips()
