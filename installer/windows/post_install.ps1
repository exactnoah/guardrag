param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$InstallerArgs
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..\..")
$logsDir = Join-Path $repoRoot "logs"
$logPath = Join-Path $logsDir "installer-post-install.log"

if (-not (Test-Path $logsDir)) {
    New-Item -Path $logsDir -ItemType Directory | Out-Null
}

Write-Host "Starting GuardRag post-install setup..."
Write-Host "Install root: $repoRoot"

$pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if (-not $pythonLauncher) {
    Write-Error "Python launcher 'py' is required but was not found. Install Python 3.10+ and rerun setup.ps1."
    exit 1
}

$installScript = Join-Path $repoRoot "scripts\install.py"
if (-not (Test-Path $installScript)) {
    Write-Error "Installer script not found: $installScript"
    exit 1
}

$argLine = $InstallerArgs -join " "
Write-Host "Running: py $installScript $argLine"

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "py"
$psi.WorkingDirectory = "$repoRoot"
$psi.Arguments = '"' + $installScript + '" ' + $argLine
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $false

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
$process.Start() | Out-Null

$stdout = $process.StandardOutput
$stderr = $process.StandardError

while (-not $process.HasExited) {
    while (-not $stdout.EndOfStream) {
        $line = $stdout.ReadLine()
        Write-Host $line
        Add-Content -Path $logPath -Value $line
    }

    while (-not $stderr.EndOfStream) {
        $line = $stderr.ReadLine()
        Write-Host $line
        Add-Content -Path $logPath -Value $line
    }

    Start-Sleep -Milliseconds 150
}

while (-not $stdout.EndOfStream) {
    $line = $stdout.ReadLine()
    Write-Host $line
    Add-Content -Path $logPath -Value $line
}

while (-not $stderr.EndOfStream) {
    $line = $stderr.ReadLine()
    Write-Host $line
    Add-Content -Path $logPath -Value $line
}

if ($process.ExitCode -ne 0) {
    Write-Error "GuardRag setup failed with exit code $($process.ExitCode). See log: $logPath"
    exit $process.ExitCode
}

Write-Host "GuardRag setup completed successfully."
exit 0
