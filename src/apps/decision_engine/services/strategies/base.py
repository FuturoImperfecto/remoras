"""Base strategy interface."""

from abc import ABC, abstractmethod
from decimal import Decimal

from apps.common.types import SignalType
from apps.trading.models import Token


class BaseStrategy(ABC):
    """Base class for all trading strategies."""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def generate_signal(self, token: Token) -> tuple[SignalType, Decimal, dict]:
        """
        Generate trading signal for a token.

        Returns:
            tuple: (signal_type, confidence, metadata)
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get strategy name."""
        pass

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        return True
