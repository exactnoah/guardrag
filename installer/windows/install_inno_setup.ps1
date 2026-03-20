param(
    [string]$DownloadUrl = "https://jrsoftware.org/download.php/is.exe"
)

$ErrorActionPreference = "Stop"

$tempInstaller = Join-Path $env:TEMP "innosetup-installer.exe"

Write-Host "Downloading Inno Setup from: $DownloadUrl"
Invoke-WebRequest -Uri $DownloadUrl -OutFile $tempInstaller

if (-not (Test-Path $tempInstaller)) {
    throw "Failed to download Inno Setup installer."
}

Write-Host "Running silent install (may prompt for elevation)..."
$proc = Start-Process -FilePath $tempInstaller -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-" -Wait -PassThru
if ($proc.ExitCode -ne 0) {
    throw "Inno Setup installer exited with code $($proc.ExitCode)."
}

$candidates = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe"
)

$found = $null
foreach ($candidate in $candidates) {
    if (Test-Path $candidate) {
        $found = $candidate
        break
    }
}

if (-not $found) {
    throw "Inno Setup install completed but ISCC.exe was not found in standard locations."
}

Write-Host "Inno Setup installed successfully: $found"
Write-Host "Next: powershell -NoProfile -ExecutionPolicy Bypass -File .\\installer\\windows\\build_installer.ps1"
