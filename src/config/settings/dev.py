"""Development settings."""

from .base import *

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Show emails in console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Less strict CORS for development
CORS_ALLOW_ALL_ORIGINS = True
