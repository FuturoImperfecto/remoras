#!/bin/bash
# Setup database script

set -e

echo "🗄️  Setting up PostgreSQL database..."

# Create database if it doesn't exist
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'crypto_trading'" | grep -q 1 || \
    psql -U postgres -c "CREATE DATABASE crypto_trading"

echo "✅ Database created/verified"

# Run migrations
echo "🔄 Running Django migrations..."
cd ../src
python manage.py migrate

echo "✅ Migrations completed"

# Create superuser (if needed)
echo "👤 Creating superuser (skip if exists)..."
python manage.py createsuperuser --noinput || true

echo "✅ Database setup completed!"
