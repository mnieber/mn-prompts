# The dev server runs on http, and the browser doesn't send a secure cookie there.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Serves the docs of the auth endpoints at /api/_allauth/openapi.html
HEADLESS_SERVE_SPECIFICATION = True
