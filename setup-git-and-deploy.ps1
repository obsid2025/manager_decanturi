# ========================================
# OBSID Decant Manager - Automated Git Setup
# ========================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   OBSID Decant Manager - Git Setup    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurare
$REPO_NAME = "obsid-decant-manager"
$PROJECT_DIR = $PSScriptRoot

# Verificare Git instalat
Write-Host "[1/7] Verificare Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "  ✗ Git nu este instalat!" -ForegroundColor Red
    Write-Host "  Instaleaza Git de la: https://git-scm.com/download/win" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "  ✓ Git este instalat" -ForegroundColor Green

# Verificare GitHub CLI
Write-Host ""
Write-Host "[2/7] Verificare GitHub CLI..." -ForegroundColor Yellow
$hasGhCli = Get-Command gh -ErrorAction SilentlyContinue

if ($hasGhCli) {
    Write-Host "  ✓ GitHub CLI (gh) este instalat" -ForegroundColor Green
    $useGhCli = $true
} else {
    Write-Host "  ⚠ GitHub CLI nu este instalat (optional)" -ForegroundColor Yellow
    Write-Host "  Vei crea repository-ul manual pe GitHub" -ForegroundColor Yellow
    $useGhCli = $false
}

# Navigare la director
Write-Host ""
Write-Host "[3/7] Navigare la directorul proiectului..." -ForegroundColor Yellow
Set-Location $PROJECT_DIR
Write-Host "  ✓ Director: $PROJECT_DIR" -ForegroundColor Green

# Initializare Git (daca nu exista deja)
Write-Host ""
Write-Host "[4/7] Initializare Git repository..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "  ⚠ Repository Git exista deja" -ForegroundColor Yellow
    $reinit = Read-Host "  Vrei sa reinitializezi? (y/N)"
    if ($reinit -eq "y" -or $reinit -eq "Y") {
        Remove-Item -Recurse -Force .git
        git init
        Write-Host "  ✓ Repository reinitializat" -ForegroundColor Green
    }
} else {
    git init
    Write-Host "  ✓ Repository Git initializat" -ForegroundColor Green
}

# Adaugare fisiere
Write-Host ""
Write-Host "[5/7] Adaugare fisiere la Git..." -ForegroundColor Yellow

$filesToAdd = @(
    "Dockerfile",
    "requirements.txt",
    "app.py",
    ".dockerignore",
    "README.md",
    "templates",
    "static"
)

foreach ($file in $filesToAdd) {
    if (Test-Path $file) {
        git add $file
        Write-Host "  ✓ Adaugat: $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Lipseste: $file" -ForegroundColor Red
    }
}

# Verificare status
Write-Host ""
Write-Host "Fisiere staged:" -ForegroundColor Cyan
git status --short

# Commit
Write-Host ""
Write-Host "[6/7] Creare commit..." -ForegroundColor Yellow
try {
    git commit -m "Initial commit - OBSID Decant Manager

Aplicatie web pentru procesarea comenzilor de decanturi parfumuri.
- Flask backend
- UI profesional (gri/negru/alb)
- Upload Excel
- Procesare automata comenzi
- Export raport productie
- Docker deployment
"
    Write-Host "  ✓ Commit creat cu succes" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Commit deja exista sau configurare Git necesara" -ForegroundColor Yellow
}

# Configurare Git user (daca nu este configurat)
$gitUser = git config user.name 2>$null
if (-not $gitUser) {
    Write-Host ""
    Write-Host "Configurare Git user:" -ForegroundColor Cyan
    $userName = Read-Host "  Numele tau (ex: John Doe)"
    $userEmail = Read-Host "  Email-ul tau (ex: john@obsid.ro)"

    git config user.name "$userName"
    git config user.email "$userEmail"

    # Re-commit cu configurare noua
    git commit --amend --reset-author --no-edit
    Write-Host "  ✓ Git configurat" -ForegroundColor Green
}

# Creare repository pe GitHub
Write-Host ""
Write-Host "[7/7] Creare repository pe GitHub..." -ForegroundColor Yellow

if ($useGhCli) {
    Write-Host "  Se verifica autentificarea GitHub CLI..." -ForegroundColor Cyan

    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠ Nu esti autentificat in GitHub CLI" -ForegroundColor Yellow
        Write-Host "  Autentificare GitHub CLI..." -ForegroundColor Cyan
        gh auth login
    }

    Write-Host "  Creare repository pe GitHub..." -ForegroundColor Cyan
    $visibility = Read-Host "  Repository public sau private? (public/private) [private]"
    if ([string]::IsNullOrWhiteSpace($visibility)) {
        $visibility = "private"
    }

    try {
        gh repo create $REPO_NAME --$visibility --source=. --remote=origin --push
        Write-Host "  ✓ Repository creat si push efectuat!" -ForegroundColor Green

        # Obtine URL-ul repository-ului
        $repoUrl = gh repo view --json url -q .url

    } catch {
        Write-Host "  ✗ Eroare la crearea repository-ului" -ForegroundColor Red
        Write-Host "  $_" -ForegroundColor Red
        $useGhCli = $false
    }
}

if (-not $useGhCli) {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  CREARE MANUALA REPOSITORY PE GITHUB                  ║" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Deschide: https://github.com/new" -ForegroundColor Cyan
    Write-Host "2. Repository name: $REPO_NAME" -ForegroundColor White
    Write-Host "3. Alege: Private sau Public" -ForegroundColor White
    Write-Host "4. NU bifa 'Add README' sau alte optiuni" -ForegroundColor White
    Write-Host "5. Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    pause

    Write-Host ""
    $githubUsername = Read-Host "Introdu username-ul tau GitHub"
    $repoUrl = "https://github.com/$githubUsername/$REPO_NAME"

    Write-Host ""
    Write-Host "Conectare la repository si push..." -ForegroundColor Cyan

    git branch -M main
    git remote add origin "$repoUrl.git"

    Write-Host ""
    Write-Host "Se face push pe GitHub..." -ForegroundColor Cyan
    Write-Host "  (S-ar putea sa ti se ceara credentialele GitHub)" -ForegroundColor Yellow

    try {
        git push -u origin main
        Write-Host "  ✓ Push efectuat cu succes!" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Eroare la push" -ForegroundColor Red
        Write-Host ""
        Write-Host "Daca push-ul esueaza cu eroare de autentificare:" -ForegroundColor Yellow
        Write-Host "  1. Genereaza un Personal Access Token:" -ForegroundColor White
        Write-Host "     https://github.com/settings/tokens" -ForegroundColor Cyan
        Write-Host "  2. Foloseste token-ul in loc de parola" -ForegroundColor White
        Write-Host ""
        pause
        git push -u origin main
    }
}

# Success!
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "        SETUP COMPLET CU SUCCES!       " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Repository GitHub:" -ForegroundColor Cyan
Write-Host "  $repoUrl" -ForegroundColor White
Write-Host ""

# Creare fisier cu instructiuni Coolify
$coolifyInstructions = @"
========================================
OBSID DECANT MANAGER - COOLIFY SETUP
========================================

✅ Repository GitHub creat cu succes!

URL: $repoUrl

========================================
PASI IN COOLIFY:
========================================

1. Login la Coolify Dashboard

2. New Resource → "Git Repository"

3. Configurare Repository:
   - Repository URL: $repoUrl
   - Branch: main
   - Build Pack: Dockerfile
   - Base Directory: / (sau lasa gol)

4. General Settings:
   - Name: OBSID Decant Manager
   - Port: 5000

5. Domains:
   - Domain: decant.obsid.ro
   - Enable HTTPS: ✅

6. Persistent Storage:
   - Add Volume Mount:
     * Mount Path: /app/uploads
   - Add Volume Mount:
     * Mount Path: /app/exports

7. Environment Variables (optional):
   - FLASK_ENV=production
   - TZ=Europe/Bucharest

8. Click "Deploy" 🚀

========================================
VERIFICARE DUPA DEPLOY:
========================================

✓ Health Check: https://decant.obsid.ro/health
✓ Aplicatie: https://decant.obsid.ro

========================================
UPDATE-URI IN VIITOR:
========================================

cd "$PROJECT_DIR"

# Faci modificari in fisiere...

git add .
git commit -m "Descriere modificare"
git push

# In Coolify: click "Redeploy"
# SAU activeaza auto-deploy on push

========================================
GATA! 🎉
========================================
"@

$coolifyInstructions | Out-File -FilePath "COOLIFY_INSTRUCTIONS.txt" -Encoding UTF8

Write-Host "Instructiuni Coolify salvate in: COOLIFY_INSTRUCTIONS.txt" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "URMATORUL PAS:" -ForegroundColor Yellow
Write-Host "Deschide Coolify si configureaza deployment" -ForegroundColor White
Write-Host "Vezi fisierul: COOLIFY_INSTRUCTIONS.txt" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Deschide fisierul cu instructiuni
notepad COOLIFY_INSTRUCTIONS.txt

Write-Host "Apasa orice tasta pentru a deschide GitHub repository in browser..." -ForegroundColor Yellow
pause

Start-Process $repoUrl

Write-Host ""
Write-Host "Succes cu deployment-ul! 🚀" -ForegroundColor Green
Write-Host ""
