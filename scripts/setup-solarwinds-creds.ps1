# Setup SolarWinds Credentials in Windows Credential Manager
# This script helps you securely store SolarWinds API credentials

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "SolarWinds Credentials Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will store your SolarWinds credentials in Windows Credential Manager."
Write-Host "This is more secure than storing passwords in environment variables or .env files."
Write-Host ""

# Get SolarWinds hostname
$hostname = Read-Host "Enter SolarWinds hostname (e.g., orion or solarwinds.company.com)"

# Get username
$username = Read-Host "Enter SolarWinds username (e.g., bfs\adm.jesse.tucker)"

# Get password securely
$securePassword = Read-Host "Enter SolarWinds password" -AsSecureString
$password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
)

# Credential reference name
$credentialRef = "solarwinds_api"

Write-Host ""
Write-Host "Adding credentials to Windows Credential Manager..." -ForegroundColor Yellow

# Add credential using cmdkey (note: cmdkey uses forward slash, but Windows Credential Manager stores it correctly)
$target = "NetOpsForge/$credentialRef"
cmdkey /generic:$target /user:$username /pass:$password | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Credentials added successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Credential Reference: $credentialRef" -ForegroundColor Cyan
    Write-Host "Target: $target" -ForegroundColor Cyan
    Write-Host ""
    
    # Update .env file with hostname and settings
    $envFile = ".env"
    $envExample = ".env.example"
    
    if (-not (Test-Path $envFile)) {
        Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
        Copy-Item $envExample $envFile
    }
    
    # Read current .env content
    $envContent = Get-Content $envFile -Raw
    
    # Update or add SolarWinds settings
    $updates = @{
        "CMDB_SOURCE" = "solarwinds"
        "SOLARWINDS_HOSTNAME" = $hostname
        "SOLARWINDS_VERIFY_SSL" = "false"
        "SOLARWINDS_CACHE_TTL" = "300"
    }
    
    foreach ($key in $updates.Keys) {
        $value = $updates[$key]
        if ($envContent -match "(?m)^$key=.*$") {
            # Update existing
            $envContent = $envContent -replace "(?m)^$key=.*$", "$key=$value"
        } else {
            # Add new
            $envContent += "`n$key=$value"
        }
    }
    
    # Save updated .env
    $envContent | Set-Content $envFile -NoNewline
    
    Write-Host "✓ Updated .env file with SolarWinds configuration" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration:" -ForegroundColor Cyan
    Write-Host "  CMDB_SOURCE=solarwinds"
    Write-Host "  SOLARWINDS_HOSTNAME=$hostname"
    Write-Host "  SOLARWINDS_VERIFY_SSL=false"
    Write-Host "  SOLARWINDS_CACHE_TTL=300"
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Test the connection:"
    Write-Host "     python test_solarwinds.py" -ForegroundColor White
    Write-Host ""
    Write-Host "  2. List devices from SolarWinds:"
    Write-Host "     netopsforge list devices" -ForegroundColor White
    Write-Host ""
    Write-Host "  3. Run automation packs:"
    Write-Host "     netopsforge run cisco-ios-health-check <device>" -ForegroundColor White
    Write-Host ""
    
} else {
    Write-Host "✗ Failed to add credentials" -ForegroundColor Red
    Write-Host "Error code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

