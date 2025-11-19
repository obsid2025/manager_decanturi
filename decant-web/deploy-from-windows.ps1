# Script PowerShell pentru deployment de pe Windows la server Ubuntu
# OBSID Decant Manager

$ErrorActionPreference = "Stop"

# Configurare
$SSH_KEY = "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub"
$SERVER = "ubuntu@130.61.223.102"
$REMOTE_DIR = "/opt/obsid-decant"
$LOCAL_DIR = $PSScriptRoot

Write-Host "=========================================="  -ForegroundColor Green
Write-Host "OBSID Decant Manager - Windows Deployment" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Verificare cheie SSH
if (-not (Test-Path $SSH_KEY)) {
    Write-Host "ERROR: Cheia SSH nu a fost gasita la: $SSH_KEY" -ForegroundColor Red
    exit 1
}

Write-Host "[1/6] Verificare conexiune SSH..." -ForegroundColor Cyan
try {
    ssh -i $SSH_KEY -o ConnectTimeout=10 $SERVER "echo 'Conexiune OK'"
    Write-Host "  ✓ Conexiune reusita" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Conexiune esuata. Verifica serverul si cheia SSH." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/6] Transfer fisiere pe server..." -ForegroundColor Cyan
Write-Host "  Sursa: $LOCAL_DIR" -ForegroundColor Gray
Write-Host "  Destinatie: $SERVER`:$REMOTE_DIR" -ForegroundColor Gray

# Creare director temporar pe server
ssh -i $SSH_KEY $SERVER "sudo mkdir -p /tmp/decant-web-upload && sudo chown ubuntu:ubuntu /tmp/decant-web-upload"

# Transfer fisiere
scp -i $SSH_KEY -r "$LOCAL_DIR\*" "${SERVER}:/tmp/decant-web-upload/" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Transfer complet" -ForegroundColor Green
} else {
    Write-Host "  ✗ Eroare la transfer" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/6] Mutare fisiere la destinatie finala..." -ForegroundColor Cyan
ssh -i $SSH_KEY $SERVER @"
    sudo mkdir -p $REMOTE_DIR
    sudo rm -rf $REMOTE_DIR/*
    sudo mv /tmp/decant-web-upload/* $REMOTE_DIR/
    sudo chown -R ubuntu:ubuntu $REMOTE_DIR
    sudo chmod +x $REMOTE_DIR/deploy.sh
    sudo chmod +x $REMOTE_DIR/setup-ssl.sh
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Fisiere mutate cu succes" -ForegroundColor Green
} else {
    Write-Host "  ✗ Eroare la mutare fisiere" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/6] Instalare dependinte Docker..." -ForegroundColor Cyan
ssh -i $SSH_KEY $SERVER "cd $REMOTE_DIR && sudo ./deploy.sh" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependinte instalate" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Posibile warning-uri (verifica manual)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[5/6] Pornire aplicatie..." -ForegroundColor Cyan
ssh -i $SSH_KEY $SERVER "cd $REMOTE_DIR && sudo docker-compose down 2>/dev/null; sudo docker-compose up -d --build"

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Aplicatie pornita" -ForegroundColor Green
} else {
    Write-Host "  ✗ Eroare la pornire aplicatie" -ForegroundColor Red
    Write-Host "  Ruleaza manual: ssh -i $SSH_KEY $SERVER 'cd $REMOTE_DIR && sudo docker-compose logs'" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[6/6] Verificare status..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

ssh -i $SSH_KEY $SERVER "cd $REMOTE_DIR && sudo docker-compose ps"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Deployment completat cu succes!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Urmatorul pas: Configurare SSL" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Inainte de a configura SSL, asigura-te ca:" -ForegroundColor Yellow
Write-Host "  1. DNS-ul pentru decant.obsid.ro pointeaza la 130.61.223.102" -ForegroundColor Yellow
Write-Host "  2. Domeniul s-a propagat (verifica: nslookup decant.obsid.ro)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pentru a configura SSL, ruleaza:" -ForegroundColor Cyan
Write-Host "  ssh -i $SSH_KEY $SERVER" -ForegroundColor White
Write-Host "  cd $REMOTE_DIR" -ForegroundColor White
Write-Host "  sudo ./setup-ssl.sh" -ForegroundColor White
Write-Host ""
Write-Host "Aplicatia va fi disponibila la: https://decant.obsid.ro" -ForegroundColor Green
Write-Host ""
