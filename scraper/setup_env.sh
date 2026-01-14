#!/bin/bash
# Setup script to create .env file from provided credentials

cat > .env << EOF
# Database Configuration
DB_HOST=localhost
DB_PORT=5433
DB_NAME=tempAdsDB
DB_USER=app_user
DB_PASSWORD="Bid919Sun(()Bid919Sun(()Bid"

# Scraper Configuration
HEADLESS=true
MAX_ADS=50
EOF

echo "✓ .env file created successfully"
echo "⚠️  Remember: .env is in .gitignore and will not be committed"

