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

    address = models.CharField(max_length=42)
    chain_id = models.IntegerField(default=1)  # 1=Ethereum, 8453=Base, etc.
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    decimals = models.IntegerField(default=18)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tokens"
        ordering = ["symbol"]
        unique_together = [["address", "chain_id"]]
        indexes = [
            models.Index(fields=["chain_id"]),
        ]

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


class TokenHolder(models.Model):
    """Tracks token holders for a specific token."""

    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="holders")
    wallet_address = models.CharField(max_length=42, db_index=True)
    balance = models.DecimalField(max_digits=78, decimal_places=0)  # Raw wei balance
    first_acquired = models.DateTimeField()
    has_initiated_transfer = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "token_holders"
        ordering = ["-balance"]
        unique_together = [["token", "wallet_address"]]
        indexes = [
            models.Index(fields=["token", "-balance"]),
            models.Index(fields=["wallet_address"]),
            models.Index(fields=["first_acquired"]),
            models.Index(fields=["has_initiated_transfer"]),
        ]

    def __str__(self):
        return f"{self.wallet_address[:10]}... holds {self.token.symbol}"

    @property
    def balance_formatted(self):
        """Return balance formatted with token decimals."""
        if self.token.decimals > 0:
            return Decimal(self.balance) / Decimal(10**self.token.decimals)
        return Decimal(self.balance)


class TokenHolderSnapshot(models.Model):
    """Historical snapshots of token holder data for trend analysis."""

    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="holder_snapshots")
    wallet_address = models.CharField(max_length=42, db_index=True)
    balance = models.DecimalField(max_digits=78, decimal_places=0)
    has_initiated_transfer = models.BooleanField(default=False)
    snapshot_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "token_holder_snapshots"
        ordering = ["-snapshot_at"]
        indexes = [
            models.Index(fields=["token", "wallet_address", "-snapshot_at"]),
            models.Index(fields=["token", "-snapshot_at"]),
        ]

    def __str__(self):
        return f"{self.wallet_address[:10]}... @ {self.snapshot_at}"


class TokenHolderSync(models.Model):
    """Tracks synchronization state for token holder data."""

    token = models.OneToOneField(Token, on_delete=models.CASCADE, related_name="holder_sync")
    last_sync_at = models.DateTimeField(null=True, blank=True)
    next_offset = models.CharField(max_length=255, null=True, blank=True)
    total_holders = models.IntegerField(default=0)
    sync_in_progress = models.BooleanField(default=False)
    last_error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "token_holder_syncs"

    def __str__(self):
        return f"Sync state for {self.token.symbol}"
