"""X Signals models."""

from django.db import models
from django.utils import timezone

from apps.common.types import SentimentScore
from apps.x_tracker.models import Tweet


class TweetFeatures(models.Model):
    """Extracted features from tweet for analysis."""

    tweet = models.OneToOneField(Tweet, on_delete=models.CASCADE, related_name="features")
    sentiment_score = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in SentimentScore],
        default=SentimentScore.NEUTRAL.value,
    )
    sentiment_confidence = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    contains_ticker = models.BooleanField(default=False)
    mentioned_tickers = models.JSONField(default=list)  # ["BTC", "ETH"]
    contains_price_prediction = models.BooleanField(default=False)
    urgency_score = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    influence_score = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    embeddings = models.JSONField(null=True, blank=True)  # Vector embeddings
    keywords = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tweet_features"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sentiment_score"]),
            models.Index(fields=["contains_ticker"]),
        ]

    def __str__(self):
        return f"Features for {self.tweet.tweet_id}"


class SignalCluster(models.Model):
    """Cluster of similar signals/tweets."""

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    centroid_embeddings = models.JSONField(null=True, blank=True)
    avg_sentiment = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    tweet_count = models.IntegerField(default=0)
    dominant_tickers = models.JSONField(default=list)
    strength_score = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "signal_clusters"
        ordering = ["-strength_score", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.tweet_count} tweets)"


class TweetClusterMembership(models.Model):
    """Many-to-many relationship between tweets and clusters."""

    tweet_features = models.ForeignKey(
        TweetFeatures, on_delete=models.CASCADE, related_name="cluster_memberships"
    )
    cluster = models.ForeignKey(
        SignalCluster, on_delete=models.CASCADE, related_name="memberships"
    )
    similarity_score = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tweet_cluster_memberships"
        unique_together = [["tweet_features", "cluster"]]
        ordering = ["-similarity_score"]

    def __str__(self):
        return f"{self.tweet_features.tweet.tweet_id} -> {self.cluster.name}"


class TrendingTopic(models.Model):
    """Trending topic detected from tweets."""

    topic = models.CharField(max_length=200, unique=True)
    ticker = models.CharField(max_length=20, null=True, blank=True)
    mention_count = models.IntegerField(default=0)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    velocity = models.DecimalField(max_digits=10, decimal_places=4, default=0)  # mentions/hour
    peak_at = models.DateTimeField(null=True, blank=True)
    is_trending = models.BooleanField(default=True)
    first_seen_at = models.DateTimeField(default=timezone.now)
    last_seen_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "trending_topics"
        ordering = ["-velocity", "-mention_count"]
        indexes = [
            models.Index(fields=["is_trending", "-velocity"]),
            models.Index(fields=["ticker"]),
        ]

    def __str__(self):
        return f"{self.topic} ({self.mention_count} mentions)"
