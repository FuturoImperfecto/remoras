#!/usr/bin/env python
"""Load initial data for the trading system."""

import os
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_path))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
import django

django.setup()

from apps.trading.models import Token, Wallet


def load_popular_tokens():
    """Load popular crypto tokens."""
    tokens = [
        {
            "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "decimals": 18,
        },
        {
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "symbol": "USDT",
            "name": "Tether USD",
            "decimals": 6,
        },
        {
            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "symbol": "USDC",
            "name": "USD Coin",
            "decimals": 6,
        },
        {
            "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            "symbol": "WBTC",
            "name": "Wrapped Bitcoin",
            "decimals": 8,
        },
        {
            "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "symbol": "DAI",
            "name": "Dai Stablecoin",
            "decimals": 18,
        },
    ]

    for token_data in tokens:
        token, created = Token.objects.get_or_create(
            address=token_data["address"],
            defaults={
                "symbol": token_data["symbol"],
                "name": token_data["name"],
                "decimals": token_data["decimals"],
            },
        )
        if created:
            print(f"✅ Created token: {token.symbol}")
        else:
            print(f"ℹ️  Token already exists: {token.symbol}")


def main():
    """Main function."""
    print("🚀 Loading initial data...")
    load_popular_tokens()
    print("✅ Initial data loaded successfully!")


if __name__ == "__main__":
    main()
