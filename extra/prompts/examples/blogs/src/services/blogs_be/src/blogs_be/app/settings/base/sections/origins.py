CORS_URLS_REGEX = r"^/(auth|api)/.*$"

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True

# Allow specific HTTP methods
CORS_ALLOW_METHODS = [
    "GET",
    "OPTIONS",
    "POST",
    # Add other methods as needed
]

# For public endpoints, we can be more permissive
CORS_ALLOW_ALL_ORIGINS = True
