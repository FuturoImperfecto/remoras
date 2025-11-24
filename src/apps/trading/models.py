"""Trading models."""

from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.common.types import OrderSide, OrderStatus


class Wallet(models.Model):
    """Crypto wallet configuration."""

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=42, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.address[:10]}...)"


class Token(models.Model):
    """Token/Cryptocurrency information."""

    address = models.CharField(max_length=42, unique=True)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    decimals = models.IntegerField(default=18)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tokens"
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} ({self.name})"


class Position(models.Model):
    """Open trading position."""

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="positions")
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="positions")
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    entry_price = models.DecimalField(max_digits=36, decimal_places=18)
    current_price = models.DecimalField(max_digits=36, decimal_places=18, null=True, blank=True)
    pnl = models.DecimalField(max_digits=36, decimal_places=18, default=Decimal("0"))
    pnl_percent = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal("0"))
    is_open = models.BooleanField(default=True)
    opened_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "positions"
        ordering = ["-opened_at"]
        indexes = [
            models.Index(fields=["wallet", "is_open"]),
            models.Index(fields=["token", "is_open"]),
        ]

    def __str__(self):
        return f"{self.token.symbol} - {self.amount} @ {self.entry_price}"


class Order(models.Model):
    """Trading order."""

    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="orders", null=True, blank=True
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="orders")
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="orders")
    side = models.CharField(max_length=10, choices=[(s.value, s.name) for s in OrderSide])
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in OrderStatus],
        default=OrderStatus.PENDING.value,
    )
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    expected_price = models.DecimalField(max_digits=36, decimal_places=18)
    executed_price = models.DecimalField(
        max_digits=36, decimal_places=18, null=True, blank=True
    )
    slippage_percent = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True
    )
    gas_used = models.BigIntegerField(null=True, blank=True)
    transaction_hash = models.CharField(max_length=66, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    executed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["wallet", "status"]),
            models.Index(fields=["transaction_hash"]),
        ]

    def __str__(self):
        return f"{self.side.upper()} {self.amount} {self.token.symbol} @ {self.expected_price}"


class TransactionLog(models.Model):
    """Blockchain transaction log."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="transaction_logs", null=True, blank=True
    )
    transaction_hash = models.CharField(max_length=66, unique=True)
    block_number = models.BigIntegerField(null=True, blank=True)
    from_address = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    value = models.DecimalField(max_digits=36, decimal_places=18)
    gas_used = models.BigIntegerField(null=True, blank=True)
    gas_price = models.BigIntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)  # True = success, False = failed
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["transaction_hash"]),
            models.Index(fields=["from_address"]),
        ]

    def __str__(self):
        return f"TX {self.transaction_hash[:10]}... - {self.status}"
