"""Pytest configuration and fixtures."""

import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from apps.trading.models import Token, Wallet
from apps.x_tracker.models import TrackedAccount
from apps.decision_engine.models import Strategy


User = get_user_model()


@pytest.fixture
def admin_user(db):
    """Create admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="testpass123"
    )


@pytest.fixture
def test_wallet(db):
    """Create test wallet."""
    return Wallet.objects.create(
        name="Test Wallet",
        address="0x1234567890123456789012345678901234567890",
        is_active=True
    )


@pytest.fixture
def test_token(db):
    """Create test token (WETH)."""
    return Token.objects.create(
        address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        symbol="WETH",
        name="Wrapped Ether",
        decimals=18,
        is_active=True
    )


@pytest.fixture
def test_tracked_account(db):
    """Create test tracked account."""
    return TrackedAccount.objects.create(
        username="cryptowhale",
        user_id="12345",
        display_name="Crypto Whale",
        followers_count=100000,
        is_verified=True,
        priority=5
    )


@pytest.fixture
def test_strategy(db):
    """Create test trading strategy."""
    return Strategy.objects.create(
        name="Test Momentum Strategy",
        description="Test strategy for momentum trading",
        strategy_type="momentum",
        is_active=True,
        min_confidence=Decimal("0.7"),
        max_position_size=Decimal("1000")
    )
