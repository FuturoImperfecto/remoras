"""Celery configuration."""

import os

from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("crypto_trading")

# Load config from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    # Trading tasks
    "update-positions-prices-every-1-min": {
        "task": "apps.trading.tasks.update_positions_prices",
        "schedule": crontab(minute="*/1"),  # Every minute
    },
    "execute-pending-orders-every-30-sec": {
        "task": "apps.trading.tasks.execute_pending_orders",
        "schedule": 30.0,  # Every 30 seconds
    },
    "sync-blockchain-transactions-every-5-min": {
        "task": "apps.trading.tasks.sync_blockchain_transactions",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
    # X Tracker tasks
    "fetch-all-tracked-accounts-every-15-min": {
        "task": "apps.x_tracker.tasks.fetch_all_tracked_accounts",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
    # X Signals tasks
    "analyze-sentiment-batch-every-5-min": {
        "task": "apps.x_signals.tasks.analyze_sentiment_batch",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
    "update-signal-clusters-every-30-min": {
        "task": "apps.x_signals.tasks.update_signal_clusters",
        "schedule": crontab(minute="*/30"),  # Every 30 minutes
    },
    "detect-trending-topics-every-10-min": {
        "task": "apps.x_signals.tasks.detect_trending_topics",
        "schedule": crontab(minute="*/10"),  # Every 10 minutes
    },
    # Decision Engine tasks
    "generate-trading-signals-every-5-min": {
        "task": "apps.decision_engine.tasks.generate_trading_signals",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
    "evaluate-signals-every-2-min": {
        "task": "apps.decision_engine.tasks.evaluate_signals",
        "schedule": crontab(minute="*/2"),  # Every 2 minutes
    },
    "execute-approved-decisions-every-1-min": {
        "task": "apps.decision_engine.tasks.execute_approved_decisions",
        "schedule": crontab(minute="*/1"),  # Every minute
    },
    "update-risk-metrics-every-5-min": {
        "task": "apps.decision_engine.tasks.update_risk_metrics",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing."""
    print(f"Request: {self.request!r}")
