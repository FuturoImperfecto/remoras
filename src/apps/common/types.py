"""Common type definitions."""

from decimal import Decimal
from enum import Enum
from typing import TypedDict


class OrderSide(str, Enum):
    """Trade order side."""

    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    """Order status."""

    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    FAILED = "failed"


class SignalType(str, Enum):
    """Trading signal type."""

    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class SentimentScore(str, Enum):
    """Sentiment classification."""

    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


class TokenInfo(TypedDict):
    """Token information."""

    address: str
    symbol: str
    decimals: int
    name: str


class PriceData(TypedDict):
    """Price data structure."""

    price: Decimal
    timestamp: int
    volume_24h: Decimal | None
