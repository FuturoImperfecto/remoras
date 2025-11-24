"""Decision Engine models."""

from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.common.types import SignalType
from apps.trading.models import Order, Token


class Strategy(models.Model):
    """Trading strategy configuration."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    strategy_type = models.CharField(max_length=50)  # momentum, sentiment, hybrid, etc.
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict)  # Strategy-specific configuration
    min_confidence = models.DecimalField(max_digits=5, decimal_places=4, default=0.7)
    max_position_size = models.DecimalField(max_digits=36, decimal_places=18, default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "strategies"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.strategy_type})"


class TradingSignal(models.Model):
    """Generated trading signal."""

    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name="signals")
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="signals")
    signal_type = models.CharField(
        max_length=10, choices=[(s.value, s.name) for s in SignalType]
    )
    confidence = models.DecimalField(max_digits=5, decimal_places=4)
    suggested_price = models.DecimalField(max_digits=36, decimal_places=18, null=True, blank=True)
    suggested_amount = models.DecimalField(
        max_digits=36, decimal_places=18, null=True, blank=True
    )
    reasoning = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict)  # Additional signal data
    is_executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "trading_signals"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["strategy", "-created_at"]),
            models.Index(fields=["token", "signal_type"]),
            models.Index(fields=["is_executed"]),
        ]

    def __str__(self):
        return f"{self.signal_type.upper()} {self.token.symbol} @ {self.confidence:.2f}"


class Decision(models.Model):
    """Trading decision made by the system."""

    signal = models.ForeignKey(
        TradingSignal, on_delete=models.CASCADE, related_name="decisions", null=True, blank=True
    )
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="decisions")
    decision_type = models.CharField(max_length=10, choices=[(s.value, s.name) for s in SignalType])
    approved = models.BooleanField(default=False)
    approval_confidence = models.DecimalField(max_digits=5, decimal_places=4)
    risk_score = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    position_size = models.DecimalField(max_digits=36, decimal_places=18)
    target_price = models.DecimalField(max_digits=36, decimal_places=18, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=36, decimal_places=18, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=36, decimal_places=18, null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, related_name="decisions", null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "decisions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["approved", "-created_at"]),
            models.Index(fields=["token"]),
        ]

    def __str__(self):
        status = "APPROVED" if self.approved else "REJECTED"
        return f"{status} {self.decision_type.upper()} {self.token.symbol}"


class RiskMetrics(models.Model):
    """Portfolio risk metrics snapshot."""

    total_exposure_usd = models.DecimalField(max_digits=36, decimal_places=18, default=0)
    total_pnl = models.DecimalField(max_digits=36, decimal_places=18, default=0)
    max_drawdown_percent = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    current_drawdown_percent = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    open_positions_count = models.IntegerField(default=0)
    win_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    measured_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "risk_metrics"
        ordering = ["-measured_at"]

    def __str__(self):
        return f"Risk Metrics {self.measured_at}"
