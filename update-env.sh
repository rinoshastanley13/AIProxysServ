#!/bin/bash
# Update .env file with new ricagoapi naming

echo "Updating .env file with ricagoapi naming..."

# Backup existing .env
if [ -f .env ]; then
    cp .env .env.backup
    echo "Created backup: .env.backup"
fi

# Update the values
sed -i '' 's/POSTGRES_DB=aiproxys/POSTGRES_DB=ricagoapi/g' .env
sed -i '' 's/POSTGRES_USER=aiproxys_user/POSTGRES_USER=ricagoapi_user/g' .env

echo "✅ Updated .env file successfully!"
echo ""
echo "Changes made:"
echo "  - POSTGRES_DB: aiproxys → ricagoapi"
echo "  - POSTGRES_USER: aiproxys_user → ricagoapi_user"
echo ""
echo "Backup saved as: .env.backup"
