"""Trading app configuration."""

from django.apps import AppConfig


class TradingConfig(AppConfig):
    """Trading app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.trading"
