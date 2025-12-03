"""Trading admin configuration."""

from django.contrib import admin

from .models import (
    Order,
    Position,
    Token,
    TokenHolder,
    TokenHolderSnapshot,
    TokenHolderSync,
    TransactionLog,
    Wallet,
)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Wallet admin."""

    list_display = ["name", "address", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "address"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """Token admin."""

    list_display = ["symbol", "name", "address", "chain_id", "decimals", "is_active"]
    list_filter = ["is_active", "chain_id"]
    search_fields = ["symbol", "name", "address"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Position admin."""

    list_display = [
        "token",
        "amount",
        "entry_price",
        "current_price",
        "pnl_percent",
        "is_open",
        "opened_at",
    ]
    list_filter = ["is_open", "token"]
    search_fields = ["wallet__address", "token__symbol"]
    readonly_fields = ["opened_at", "closed_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin."""

    list_display = [
        "token",
        "side",
        "amount",
        "status",
        "expected_price",
        "executed_price",
        "created_at",
    ]
    list_filter = ["status", "side", "token"]
    search_fields = ["wallet__address", "token__symbol", "transaction_hash"]
    readonly_fields = ["created_at", "executed_at"]


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    """Transaction log admin."""

    list_display = ["transaction_hash", "from_address", "to_address", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["transaction_hash", "from_address", "to_address"]
    readonly_fields = ["created_at"]


@admin.register(TokenHolder)
class TokenHolderAdmin(admin.ModelAdmin):
    """Token holder admin."""

    list_display = [
        "wallet_address",
        "token",
        "balance",
        "first_acquired",
        "has_initiated_transfer",
        "last_updated",
    ]
    list_filter = ["has_initiated_transfer", "token", "token__chain_id"]
    search_fields = ["wallet_address", "token__symbol", "token__address"]
    readonly_fields = ["created_at", "last_updated"]
    raw_id_fields = ["token"]


@admin.register(TokenHolderSnapshot)
class TokenHolderSnapshotAdmin(admin.ModelAdmin):
    """Token holder snapshot admin."""

    list_display = ["wallet_address", "token", "balance", "has_initiated_transfer", "snapshot_at"]
    list_filter = ["token", "has_initiated_transfer"]
    search_fields = ["wallet_address", "token__symbol"]
    readonly_fields = ["snapshot_at"]
    raw_id_fields = ["token"]


@admin.register(TokenHolderSync)
class TokenHolderSyncAdmin(admin.ModelAdmin):
    """Token holder sync admin."""

    list_display = [
        "token",
        "total_holders",
        "last_sync_at",
        "sync_in_progress",
        "updated_at",
    ]
    list_filter = ["sync_in_progress"]
    search_fields = ["token__symbol", "token__address"]
    readonly_fields = ["created_at", "updated_at"]
