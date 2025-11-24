"""Health check utilities."""

from typing import Any

from django.db import connection
from django.db.utils import OperationalError

from .redis import get_redis_client


def check_database() -> dict[str, Any]:
    """Check database connectivity."""
    try:
        connection.ensure_connection()
        return {"status": "healthy", "service": "database"}
    except OperationalError as e:
        return {"status": "unhealthy", "service": "database", "error": str(e)}


def check_redis() -> dict[str, Any]:
    """Check Redis connectivity."""
    try:
        client = get_redis_client()
        client.ping()
        return {"status": "healthy", "service": "redis"}
    except Exception as e:
        return {"status": "unhealthy", "service": "redis", "error": str(e)}


def check_celery() -> dict[str, Any]:
    """Check Celery worker status."""
    try:
        from infra.celery import app

        stats = app.control.inspect().stats()
        if stats:
            return {"status": "healthy", "service": "celery", "workers": len(stats)}
        return {"status": "unhealthy", "service": "celery", "error": "No workers found"}
    except Exception as e:
        return {"status": "unhealthy", "service": "celery", "error": str(e)}


def get_system_health() -> dict[str, Any]:
    """Get overall system health status."""
    checks = [
        check_database(),
        check_redis(),
        check_celery(),
    ]

    all_healthy = all(check["status"] == "healthy" for check in checks)

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks,
    }
