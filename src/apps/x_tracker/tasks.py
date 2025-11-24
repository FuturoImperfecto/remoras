"""X Tracker Celery tasks."""

from celery import shared_task


@shared_task
def fetch_tweets_for_account(account_id: int):
    """Fetch latest tweets for a tracked account."""
    # TODO: Implement tweet fetching logic
    pass


@shared_task
def fetch_all_tracked_accounts():
    """Fetch tweets for all active tracked accounts."""
    # TODO: Implement bulk fetching logic
    pass


@shared_task
def update_account_metrics(account_id: int):
    """Update metrics for a tracked account."""
    # TODO: Implement metrics update logic
    pass
