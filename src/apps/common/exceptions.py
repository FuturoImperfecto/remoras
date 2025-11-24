"""Custom exceptions for the crypto trading system."""


class TradingSystemException(Exception):
    """Base exception for trading system."""

    pass


class BlockchainException(TradingSystemException):
    """Blockchain/Web3 related exceptions."""

    pass


class InsufficientBalanceException(BlockchainException):
    """Insufficient balance for trade execution."""

    pass


class TransactionFailedException(BlockchainException):
    """Transaction failed on blockchain."""

    pass


class APIException(TradingSystemException):
    """External API exceptions."""

    pass


class XAPIException(APIException):
    """X (Twitter) API exceptions."""

    pass


class RateLimitException(APIException):
    """API rate limit exceeded."""

    pass


class DataProcessingException(TradingSystemException):
    """Data processing/analysis exceptions."""

    pass


class StrategyException(TradingSystemException):
    """Trading strategy exceptions."""

    pass


class RiskManagementException(TradingSystemException):
    """Risk management exceptions."""

    pass


class MaxDrawdownExceeded(RiskManagementException):
    """Maximum drawdown threshold exceeded."""

    pass


class PositionSizeTooLarge(RiskManagementException):
    """Position size exceeds allowed limit."""

    pass
