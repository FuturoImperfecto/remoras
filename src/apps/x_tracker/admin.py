"""X Tracker admin configuration."""

from django.contrib import admin

from .models import AccountMetrics, TrackedAccount, Tweet


@admin.register(TrackedAccount)
class TrackedAccountAdmin(admin.ModelAdmin):
    """Tracked account admin."""

    list_display = [
        "username",
        "display_name",
        "followers_count",
        "is_verified",
        "priority",
        "is_active",
        "last_fetched_at",
    ]
    list_filter = ["is_active", "is_verified"]
    search_fields = ["username", "display_name", "user_id"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    """Tweet admin."""

    list_display = [
        "account",
        "text_preview",
        "created_at_twitter",
        "like_count",
        "retweet_count",
    ]
    list_filter = ["is_retweet", "has_media", "language"]
    search_fields = ["text", "tweet_id", "account__username"]
    readonly_fields = ["created_at"]

    def text_preview(self, obj):
        """Short preview of tweet text."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Text"


@admin.register(AccountMetrics)
class AccountMetricsAdmin(admin.ModelAdmin):
    """Account metrics admin."""

    list_display = [
        "account",
        "followers_count",
        "tweet_count",
        "engagement_rate",
        "measured_at",
    ]
    list_filter = ["measured_at"]
    search_fields = ["account__username"]
