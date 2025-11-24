"""Common utilities."""

from decimal import Decimal


def wei_to_ether(wei: int) -> Decimal:
    """Convert Wei to Ether."""
    return Decimal(wei) / Decimal(10**18)


def ether_to_wei(ether: Decimal | float) -> int:
    """Convert Ether to Wei."""
    return int(Decimal(ether) * Decimal(10**18))


def calculate_slippage(expected_price: Decimal, actual_price: Decimal) -> Decimal:
    """Calculate slippage percentage."""
    if expected_price == 0:
        return Decimal(0)
    return abs((actual_price - expected_price) / expected_price) * 100
