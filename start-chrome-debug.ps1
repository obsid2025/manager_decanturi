# Script pentru pornirea Chrome cu Remote Debugging
# Folosit pentru debugging Selenium automation pe Windows

Write-Host "🚀 Pornire Chrome cu Remote Debugging..." -ForegroundColor Cyan
Write-Host ""

# Închide toate instanțele Chrome existente
Write-Host "⏹️ Închidere Chrome existent..." -ForegroundColor Yellow
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Path către Chrome
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Verifică dacă Chrome există
if (-not (Test-Path $chromePath)) {
    Write-Host "❌ Chrome nu a fost găsit la: $chromePath" -ForegroundColor Red
    Write-Host "💡 Verifică path-ul către Chrome și încearcă din nou." -ForegroundColor Yellow
    pause
    exit
}

# User Data Directory
$userDataDir = "$env:LOCALAPPDATA\Google\Chrome\User Data"

# Pornește Chrome cu remote debugging
Write-Host "✅ Pornire Chrome cu remote debugging pe port 9222..." -ForegroundColor Green
Write-Host ""

& $chromePath --remote-debugging-port=9222 --user-data-dir="$userDataDir"

Write-Host ""
Write-Host "✅ Chrome pornit cu succes!" -ForegroundColor Green
Write-Host "🔗 Remote debugging activ pe: http://localhost:9222" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Următorii pași:" -ForegroundColor Yellow
Write-Host "1. Loghează-te în Oblio (https://www.oblio.eu)" -ForegroundColor White
Write-Host "2. Pornește aplicația Python (python app.py)" -ForegroundColor White
Write-Host "3. Folosește automatizarea - vei vedea LIVE în acest Chrome!" -ForegroundColor White
Write-Host ""
