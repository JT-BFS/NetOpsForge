# NetOpsForge GPG Setup Script
# This script sets up GPG commit signing for GitHub

Write-Host "Setting up GPG commit signing for NetOpsForge..." -ForegroundColor Cyan
Write-Host ""

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Check if GPG key already exists
$existingKeys = gpg --list-secret-keys --keyid-format=long 2>&1
if ($existingKeys -match "sec") {
    Write-Host "GPG key already exists!" -ForegroundColor Green
    Write-Host ""
    gpg --list-secret-keys --keyid-format=long
    Write-Host ""
    Write-Host "To use an existing key, run:" -ForegroundColor Yellow
    Write-Host "   git config --global user.signingkey <KEY_ID>" -ForegroundColor White
    Write-Host "   git config --global commit.gpgsign true" -ForegroundColor White
    exit 0
}

Write-Host "Creating GPG key for:" -ForegroundColor Yellow
Write-Host "   Name:  Jesse Tucker" -ForegroundColor White
Write-Host "   Email: jesse.tucker@bldr.com" -ForegroundColor White
Write-Host ""

# Create GPG key batch file
$batchContent = @"
%echo Generating GPG key for NetOpsForge
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: Jesse Tucker
Name-Email: jesse.tucker@bldr.com
Expire-Date: 0
%no-protection
%commit
%echo Done
"@

$batchFile = Join-Path $env:TEMP "gpg-batch.txt"
$batchContent | Out-File -FilePath $batchFile -Encoding ASCII

Write-Host "Generating GPG key (this may take a moment)..." -ForegroundColor Cyan
gpg --batch --generate-key $batchFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "GPG key generated successfully!" -ForegroundColor Green
    Write-Host ""

    # Get the key ID
    $keyInfo = gpg --list-secret-keys --keyid-format=long "jesse.tucker@bldr.com" 2>&1
    $keyId = ($keyInfo | Select-String -Pattern "sec\s+rsa4096/([A-F0-9]+)" | ForEach-Object { $_.Matches.Groups[1].Value })

    if ($keyId) {
        Write-Host "Your GPG Key ID: $keyId" -ForegroundColor Green
        Write-Host ""

        # Configure Git to use this key
        Write-Host "Configuring Git to use GPG signing..." -ForegroundColor Cyan
        git config --global user.signingkey $keyId
        git config --global commit.gpgsign true
        git config --global gpg.program "gpg"

        Write-Host "Git configured for GPG signing!" -ForegroundColor Green
        Write-Host ""

        # Export public key for GitHub
        Write-Host "Your GPG Public Key (add this to GitHub):" -ForegroundColor Yellow
        Write-Host "========================================================================" -ForegroundColor DarkGray
        gpg --armor --export $keyId
        Write-Host "========================================================================" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "Next Steps:" -ForegroundColor Cyan
        Write-Host "   1. Copy the GPG public key above (including BEGIN/END lines)" -ForegroundColor White
        Write-Host "   2. Go to: https://github.com/settings/keys" -ForegroundColor White
        Write-Host "   3. Click New GPG key" -ForegroundColor White
        Write-Host "   4. Paste the key and save" -ForegroundColor White
        Write-Host ""
        Write-Host "After adding to GitHub, all your commits will be signed!" -ForegroundColor Green

        # Save key ID for later use
        $keyId | Out-File -FilePath (Join-Path $PSScriptRoot ".gpg-key-id") -Encoding ASCII
    } else {
        Write-Host "Could not extract key ID. Please run manually:" -ForegroundColor Yellow
        Write-Host "   gpg --list-secret-keys --keyid-format=long" -ForegroundColor White
    }
} else {
    Write-Host "Failed to generate GPG key" -ForegroundColor Red
    exit 1
}

# Clean up
Remove-Item $batchFile -ErrorAction SilentlyContinue

