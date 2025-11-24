"""API serializers."""

from rest_framework import serializers

from apps.decision_engine.models import Decision, TradingSignal
from apps.trading.models import Order, Position, Token


class TokenSerializer(serializers.ModelSerializer):
    """Token serializer."""

    class Meta:
        model = Token
        fields = ["id", "address", "symbol", "name", "decimals"]


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
