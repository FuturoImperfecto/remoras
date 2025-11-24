"""Trading admin configuration."""

from django.contrib import admin

from .models import Order, Position, Token, TransactionLog, Wallet


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

    list_display = ["symbol", "name", "address", "decimals", "is_active"]
    list_filter = ["is_active"]
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
