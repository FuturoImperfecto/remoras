"""X Tracker models."""

from django.db import models
from django.utils import timezone


class TrackedAccount(models.Model):
    """X (Twitter) account being tracked."""

    username = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    followers_count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)  # Higher = more important
    last_fetched_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tracked_accounts"
        ordering = ["-priority", "-followers_count"]

    def __str__(self):
        return f"@{self.username}"


class Tweet(models.Model):
    """Tweet from tracked account."""

    account = models.ForeignKey(TrackedAccount, on_delete=models.CASCADE, related_name="tweets")
    tweet_id = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    created_at_twitter = models.DateTimeField()
    retweet_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    quote_count = models.IntegerField(default=0)
    is_retweet = models.BooleanField(default=False)
    retweeted_tweet_id = models.CharField(max_length=100, null=True, blank=True)
    has_media = models.BooleanField(default=False)
    has_url = models.BooleanField(default=False)
    language = models.CharField(max_length=10, null=True, blank=True)
    raw_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tweets"
        ordering = ["-created_at_twitter"]
        indexes = [
            models.Index(fields=["account", "-created_at_twitter"]),
            models.Index(fields=["tweet_id"]),
            models.Index(fields=["-created_at_twitter"]),
        ]

    def __str__(self):
        return f"@{self.account.username}: {self.text[:50]}..."


class AccountMetrics(models.Model):
    """Historical metrics for tracked accounts."""

    account = models.ForeignKey(
        TrackedAccount, on_delete=models.CASCADE, related_name="metrics"
    )
    followers_count = models.IntegerField()
    following_count = models.IntegerField()
    tweet_count = models.IntegerField()
    listed_count = models.IntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    measured_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "account_metrics"
        ordering = ["-measured_at"]
        indexes = [
            models.Index(fields=["account", "-measured_at"]),
        ]

    def __str__(self):
        return f"{self.account.username} - {self.measured_at}"
