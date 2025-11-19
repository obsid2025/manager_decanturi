#!/bin/bash

# Script de deployment pentru OBSID Decant Manager
# Rulează pe serverul Ubuntu

set -e

echo "=========================================="
echo "OBSID Decant Manager - Deployment Script"
echo "=========================================="

# Variabile
APP_DIR="/opt/obsid-decant"
DOMAIN="decant.obsid.ro"
EMAIL="contact@obsid.ro"  # Înlocuiește cu email-ul tău

# Culori pentru output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificare user root
if [[ $EUID -ne 0 ]]; then
   print_error "Acest script trebuie rulat ca root (sudo)"
   exit 1
fi

# 1. Update sistem
print_info "Actualizare sistem..."
apt-get update
apt-get upgrade -y

# 2. Instalare Docker (dacă nu există)
if ! command -v docker &> /dev/null; then
    print_info "Instalare Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
else
    print_info "Docker este deja instalat"
fi

# 3. Instalare Docker Compose (dacă nu există)
if ! command -v docker-compose &> /dev/null; then
    print_info "Instalare Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    print_info "Docker Compose este deja instalat"
fi

# 4. Creare director aplicație
print_info "Creare director aplicație: $APP_DIR"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# 5. Oprire containere existente (dacă există)
if [ -f "docker-compose.yml" ]; then
    print_warning "Oprire containere existente..."
    docker-compose down || true
fi

# 6. Mesaj pentru utilizator
print_info "=========================================="
print_info "Setup completat cu succes!"
print_info "=========================================="
echo ""
print_info "Pași următori:"
echo "1. Copiază fișierele aplicației în: $APP_DIR"
echo "2. Configurează DNS-ul pentru $DOMAIN să pointeze la acest server"
echo "3. Rulează: cd $APP_DIR && docker-compose up -d"
echo "4. Generează certificat SSL: ./setup-ssl.sh"
echo ""
print_info "După pornire, aplicația va fi disponibilă la: https://$DOMAIN"
