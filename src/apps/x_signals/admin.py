"""X Signals admin configuration."""

from django.contrib import admin

from .models import SignalCluster, TrendingTopic, TweetClusterMembership, TweetFeatures


@admin.register(TweetFeatures)
class TweetFeaturesAdmin(admin.ModelAdmin):
    """Tweet features admin."""

    list_display = [
        "tweet",
        "sentiment_score",
        "sentiment_confidence",
        "contains_ticker",
        "influence_score",
    ]
    list_filter = ["sentiment_score", "contains_ticker", "contains_price_prediction"]
    search_fields = ["tweet__text", "mentioned_tickers"]


@admin.register(SignalCluster)
class SignalClusterAdmin(admin.ModelAdmin):
    """Signal cluster admin."""

    list_display = [
        "name",
        "tweet_count",
        "avg_sentiment",
        "strength_score",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active"]
    search_fields = ["name", "description", "dominant_tickers"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(TweetClusterMembership)
class TweetClusterMembershipAdmin(admin.ModelAdmin):
    """Tweet cluster membership admin."""

    list_display = ["tweet_features", "cluster", "similarity_score", "added_at"]
    list_filter = ["cluster"]
    search_fields = ["tweet_features__tweet__text"]


@admin.register(TrendingTopic)
class TrendingTopicAdmin(admin.ModelAdmin):
    """Trending topic admin."""

    list_display = [
        "topic",
        "ticker",
        "mention_count",
        "velocity",
        "is_trending",
        "last_seen_at",
    ]
    list_filter = ["is_trending"]
    search_fields = ["topic", "ticker"]
