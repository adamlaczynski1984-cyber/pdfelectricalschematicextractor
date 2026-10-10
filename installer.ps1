# PDF Electrical Schematic Extractor - Windows Installer
# Run as Administrator

$ErrorActionPreference = "Stop"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "PDF Electrical Schematic Extractor - Instalator" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "BLAD: Uruchom instalator jako Administrator!" -ForegroundColor Red
    Read-Host "Nacisnij Enter aby zakonczyc"
    exit 1
}

$installPath = "C:\Program Files\PDFElectricalSchematicExtractor"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
$scriptPath = $PSScriptRoot

Write-Host "[1/6] Sprawdzanie Python..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "Python nie jest zainstalowany. Pobieram i instaluje..." -ForegroundColor Yellow
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    $downloadUrl = "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $pythonInstaller
    Start-Process $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Host "BLAD: Python nie zostal poprawnie zainstalowany." -ForegroundColor Red
        Read-Host "Nacisnij Enter aby zakonczyc"
        exit 1
    }
}
Write-Host "✓ Python OK" -ForegroundColor Green

Write-Host "[2/6] Przygotowanie katalogu instalacji..." -ForegroundColor Yellow
if (-not (Test-Path $installPath)) {
    New-Item -ItemType Directory -Path $installPath -Force | Out-Null
}
Write-Host "✓ Katalog: $installPath" -ForegroundColor Green

Write-Host "[3/6] Kopiowanie plikow aplikacji..." -ForegroundColor Yellow
Copy-Item -Path "$scriptPath\*" -Destination $installPath -Recurse -Force -Exclude @("installer.ps1", "venv", "__pycache__", "*.pyc", ".git", ".github")
Write-Host "✓ Pliki skopiowane" -ForegroundColor Green

Write-Host "[4/6] Tworzenie srodowiska venv..." -ForegroundColor Yellow
cd $installPath
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "BLAD: Nie udalo sie utworzyc venv" -ForegroundColor Red
    exit 1
}
Write-Host "✓ venv utworzone" -ForegroundColor Green

Write-Host "[5/6] Instalacja bibliotek Python..." -ForegroundColor Yellow
& "$installPath\venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip --quiet
pip install -r "$installPath\requirements.txt" --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "BLAD: Nie udalo sie zainstalowac bibliotek Python." -ForegroundColor Red
    Read-Host "Nacisnij Enter aby zakonczyc"
    exit 1
}
Write-Host "✓ Biblioteki zainstalowane" -ForegroundColor Green

Write-Host "[6/6] Instalacja Tesseract / Poppler..." -ForegroundColor Yellow
$ts = Get-Command tesseract -ErrorAction SilentlyContinue
if (-not $ts) {
    Write-Host "Tesseract nie znaleziony. Probuje zainstalowac za pomoca winget..." -ForegroundColor Yellow
    try {
        winget install --id UB-Mannheim.TesseractOCR -e --accept-source-agreements --accept-package-agreements
    }
    catch {
        Write-Host "! winget nie dostepny lub instalacja Tesseract nie powiodla sie." -ForegroundColor Yellow
        Write-Host "Zaloguj sie do: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    }
}

$pdftoppm = Get-Command pdftoppm -ErrorAction SilentlyContinue
if (-not $pdftoppm) {
    Write-Host "Poppler nie znaleziony. Probuje zainstalowac za pomoca winget..." -ForegroundColor Yellow
    try {
        winget install --id oschwartz10612.poppler-windows -e --accept-source-agreements --accept-package-agreements
    }
    catch {
        Write-Host "! winget nie dostepny lub instalacja Poppler nie powiodla sie." -ForegroundColor Yellow
        Write-Host "Zaloguj sie do: https://github.com/oschwartz10612/poppler-windows/releases" -ForegroundColor Yellow
    }
}

Write-Host "Generowanie ikony aplikacji..." -ForegroundColor Yellow
python "$installPath\create_icon.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "! Nie utworzono ikony, ale aplikacja moze nadal dzialac." -ForegroundColor Yellow
}

# Create desktop shortcut
$shortcutPath = "$desktopPath\PDF Electrical Schematic Extractor.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "$installPath\run.bat"
$shortcut.WorkingDirectory = $installPath
$shortcut.Description = "PDF Electrical Schematic Extractor"
$shortcut.IconLocation = "$installPath\app.ico,0"
$shortcut.Save()

# Start Menu shortcut
$startMenuShortcutPath = "$startMenuPath\PDF Electrical Schematic Extractor.lnk"
$startMenuShortcut = $WshShell.CreateShortcut($startMenuShortcutPath)
$startMenuShortcut.TargetPath = "$installPath\run.bat"
$startMenuShortcut.WorkingDirectory = $installPath
$startMenuShortcut.Description = "PDF Electrical Schematic Extractor"
$startMenuShortcut.IconLocation = "$installPath\app.ico,0"
$startMenuShortcut.Save()

Write-Host "\n===================================================" -ForegroundColor Green
Write-Host "INSTALACJA ZAKONCZONA" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Aplikacja jest dostepna na pulpicie: PDF Electrical Schematic Extractor" -ForegroundColor Cyan
Write-Host "Uwazaj: jesli Tesseract lub Poppler nie zostaly poprawnie zainstalowane, uruchom je ponownie z oficjalnych instalatorow." -ForegroundColor Yellow
Write-Host ""
Write-Host "Aplikacja uruchomi sie na: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Read-Host "Nacisnij Enter aby zakonczyc"
