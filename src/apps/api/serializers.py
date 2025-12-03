"""API serializers."""

from rest_framework import serializers

from apps.decision_engine.models import Decision, TradingSignal
from apps.trading.models import (
    Order,
    Position,
    Token,
    TokenHolder,
    TokenHolderSnapshot,
    TokenHolderSync,
)


class TokenSerializer(serializers.ModelSerializer):
    """Token serializer."""

    class Meta:
        model = Token
        fields = ["id", "address", "chain_id", "symbol", "name", "decimals"]


class PositionSerializer(serializers.ModelSerializer):
    """Position serializer."""

    token = TokenSerializer(read_only=True)

    class Meta:
        model = Position
        fields = [
            "id",
            "token",
            "amount",
            "entry_price",
            "current_price",
            "pnl",
            "pnl_percent",
            "is_open",
            "opened_at",
            "closed_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    token = TokenSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "token",
            "side",
            "status",
            "amount",
            "expected_price",
            "executed_price",
            "slippage_percent",
            "transaction_hash",
            "created_at",
            "executed_at",
        ]


class TradingSignalSerializer(serializers.ModelSerializer):
    """Trading signal serializer."""

    token = TokenSerializer(read_only=True)
    strategy_name = serializers.CharField(source="strategy.name", read_only=True)

    class Meta:
        model = TradingSignal
        fields = [
            "id",
            "strategy_name",
            "token",
            "signal_type",
            "confidence",
            "suggested_price",
            "suggested_amount",
            "reasoning",
            "is_executed",
            "created_at",
        ]


class DecisionSerializer(serializers.ModelSerializer):
    """Decision serializer."""

    token = TokenSerializer(read_only=True)

    class Meta:
        model = Decision
        fields = [
            "id",
            "token",
            "decision_type",
            "approved",
            "approval_confidence",
            "risk_score",
            "position_size",
            "target_price",
            "stop_loss",
            "take_profit",
            "rejection_reason",
            "created_at",
        ]


class TokenHolderSerializer(serializers.ModelSerializer):
    """Token holder serializer."""

    token = TokenSerializer(read_only=True)
    balance_formatted = serializers.DecimalField(
        max_digits=36, decimal_places=18, read_only=True
    )

    class Meta:
        model = TokenHolder
        fields = [
            "id",
            "token",
            "wallet_address",
            "balance",
            "balance_formatted",
            "first_acquired",
            "has_initiated_transfer",
            "last_updated",
            "created_at",
        ]


class TokenHolderSnapshotSerializer(serializers.ModelSerializer):
    """Token holder snapshot serializer."""

    class Meta:
        model = TokenHolderSnapshot
        fields = [
            "id",
            "wallet_address",
            "balance",
            "has_initiated_transfer",
            "snapshot_at",
        ]


class TokenHolderSyncSerializer(serializers.ModelSerializer):
    """Token holder sync state serializer."""

    token = TokenSerializer(read_only=True)

    class Meta:
        model = TokenHolderSync
        fields = [
            "id",
            "token",
            "last_sync_at",
            "total_holders",
            "sync_in_progress",
            "last_error",
            "updated_at",
        ]


class TokenHolderBulkCreateSerializer(serializers.Serializer):
    """Serializer for bulk creating/updating token holders."""

    token_address = serializers.CharField(max_length=42)
    chain_id = serializers.IntegerField()
    holders = serializers.ListField(child=serializers.DictField())
    next_offset = serializers.CharField(required=False, allow_null=True)
