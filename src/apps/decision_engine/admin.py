"""Decision Engine admin configuration."""

from django.contrib import admin

from .models import Decision, RiskMetrics, Strategy, TradingSignal


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    """Strategy admin."""

    list_display = [
        "name",
        "strategy_type",
        "is_active",
        "min_confidence",
        "max_position_size",
    ]
    list_filter = ["is_active", "strategy_type"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(TradingSignal)
class TradingSignalAdmin(admin.ModelAdmin):
    """Trading signal admin."""

    list_display = [
        "token",
        "signal_type",
        "confidence",
        "strategy",
        "is_executed",
        "created_at",
    ]
    list_filter = ["signal_type", "is_executed", "strategy"]
    search_fields = ["token__symbol", "reasoning"]
    readonly_fields = ["created_at"]


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    """Decision admin."""

    list_display = [
        "token",
        "decision_type",
        "approved",
        "approval_confidence",
        "risk_score",
        "created_at",
    ]
    list_filter = ["approved", "decision_type"]
    search_fields = ["token__symbol", "rejection_reason"]
    readonly_fields = ["created_at"]


@admin.register(RiskMetrics)
class RiskMetricsAdmin(admin.ModelAdmin):
    """Risk metrics admin."""

    list_display = [
        "measured_at",
        "total_exposure_usd",
        "total_pnl",
        "current_drawdown_percent",
        "open_positions_count",
        "win_rate",
    ]
    readonly_fields = ["measured_at"]
