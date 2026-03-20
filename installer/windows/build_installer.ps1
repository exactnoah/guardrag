param(
    [string]$InnoCompilerPath
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..\..")
$issFile = Join-Path $scriptRoot "GuardRagSetup.iss"

if (-not (Test-Path $issFile)) {
    throw "Inno Setup script not found: $issFile"
}

if (-not $InnoCompilerPath) {
    $candidates = @(
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            $InnoCompilerPath = $candidate
            break
        }
    }
}

if (-not $InnoCompilerPath -or -not (Test-Path $InnoCompilerPath)) {
    throw "ISCC.exe not found. Run .\\installer\\windows\\install_inno_setup.ps1 or install Inno Setup 6 manually, then rerun this script."
}

Write-Host "Using Inno Setup compiler: $InnoCompilerPath"
Write-Host "Building installer from: $issFile"

Push-Location $repoRoot
try {
    & "$InnoCompilerPath" "$issFile"
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup compiler failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

Write-Host "Installer build completed. Output: installer\windows\dist"
