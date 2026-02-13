# NetOpsForge CMDB Setup Script
# This script helps you set up your private CMDB from the example template

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "🔧 NetOpsForge CMDB Setup" -ForegroundColor Cyan
Write-Host ""

$exampleFile = "cmdb\devices.example.yml"
$targetFile = "cmdb\devices.yml"

# Check if example file exists
if (-not (Test-Path $exampleFile)) {
    Write-Host "❌ Error: Example file not found: $exampleFile" -ForegroundColor Red
    exit 1
}

# Check if target file already exists
if (Test-Path $targetFile) {
    if (-not $Force) {
        Write-Host "⚠️  Warning: $targetFile already exists!" -ForegroundColor Yellow
        Write-Host ""
        $response = Read-Host "Do you want to overwrite it? (yes/no)"
        if ($response -ne "yes") {
            Write-Host "❌ Aborted. Your existing $targetFile was not modified." -ForegroundColor Yellow
            exit 0
        }
    }
    Write-Host "⚠️  Overwriting existing $targetFile..." -ForegroundColor Yellow
}

# Copy the example file
try {
    Copy-Item -Path $exampleFile -Destination $targetFile -Force
    Write-Host "✅ Created $targetFile from template" -ForegroundColor Green
} catch {
    Write-Host "❌ Error copying file: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Edit $targetFile with your real network devices:" -ForegroundColor White
Write-Host "   notepad $targetFile" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Replace example IPs (10.0.x.x) with your actual management IPs" -ForegroundColor White
Write-Host ""
Write-Host "3. Update hostnames, platforms, and credential references" -ForegroundColor White
Write-Host ""
Write-Host "4. Add credentials to Windows Credential Manager:" -ForegroundColor White
Write-Host "   netopsforge creds add cisco_readonly" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Test your CMDB:" -ForegroundColor White
Write-Host "   netopsforge list devices" -ForegroundColor Gray
Write-Host ""
Write-Host "🔒 Security Note:" -ForegroundColor Yellow
Write-Host "   Your $targetFile is automatically git-ignored." -ForegroundColor Yellow
Write-Host "   It will NEVER be committed to the repository." -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green

