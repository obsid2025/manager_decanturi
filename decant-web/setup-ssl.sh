#!/bin/bash

# Script pentru configurare SSL cu Let's Encrypt
# Rulează după ce aplicația este deployată și DNS-ul este configurat

set -e

DOMAIN="decant.obsid.ro"
EMAIL="contact@obsid.ro"  # Înlocuiește cu email-ul tău

echo "=========================================="
echo "Setup SSL Certificate pentru $DOMAIN"
echo "=========================================="

# Verificare dacă nginx rulează
if ! docker ps | grep -q obsid-decant-nginx; then
    echo "ERROR: Nginx nu rulează. Pornește aplicația mai întâi cu: docker-compose up -d"
    exit 1
fi

# Creare director pentru certbot
mkdir -p certbot/conf certbot/www

# Obținere certificat
echo "Obținere certificat SSL de la Let's Encrypt..."
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Restart nginx pentru a încărca certificatul
echo "Restart Nginx..."
docker-compose restart nginx

echo ""
echo "=========================================="
echo "SSL Setup completat cu succes!"
echo "=========================================="
echo "Certificatul va fi reînnoit automat de containerul certbot."
echo "Site-ul este acum disponibil la: https://$DOMAIN"
