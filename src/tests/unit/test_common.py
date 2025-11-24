"""Unit tests for common utilities."""

import pytest
from decimal import Decimal

from apps.common.utils import wei_to_ether, ether_to_wei, calculate_slippage


class TestConversions:
    """Test Wei/Ether conversions."""

    def test_wei_to_ether(self):
        """Test Wei to Ether conversion."""
        assert wei_to_ether(1000000000000000000) == Decimal("1")
        assert wei_to_ether(500000000000000000) == Decimal("0.5")

    def test_ether_to_wei(self):
        """Test Ether to Wei conversion."""
        assert ether_to_wei(Decimal("1")) == 1000000000000000000
        assert ether_to_wei(0.5) == 500000000000000000


class TestSlippage:
    """Test slippage calculations."""

    def test_calculate_slippage_no_change(self):
        """Test slippage when prices are equal."""
        assert calculate_slippage(Decimal("100"), Decimal("100")) == Decimal("0")

    def test_calculate_slippage_increase(self):
        """Test slippage when price increases."""
        result = calculate_slippage(Decimal("100"), Decimal("105"))
        assert result == Decimal("5")

    def test_calculate_slippage_decrease(self):
        """Test slippage when price decreases."""
        result = calculate_slippage(Decimal("100"), Decimal("95"))
        assert result == Decimal("5")
