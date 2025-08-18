# Build a wheel-only distribution, validate it, and optionally install locally.

param(
    [switch]$InstallLocal = $false,
    [switch]$NoDeps = $false
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "=> Installing build tooling..."
python -m pip install --upgrade pip setuptools wheel build twine

Write-Host "=> Cleaning previous artifacts..."
Remove-Item -Recurse -Force .\dist\,.\build\,.\*.egg-info -ErrorAction SilentlyContinue

Write-Host "=> Building wheel..."
python -m build --wheel

Write-Host "=> Verifying wheel metadata..."
python -m twine check .\dist\*.whl

if ($InstallLocal) {
    Write-Host "=> Installing the newest wheel locally..."
    $wheel = Get-ChildItem -Path .\dist\*.whl | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $wheel) {
        throw "No wheel found in .\dist"
    }

    $args = @('install', '--force-reinstall')
    if ($NoDeps) { $args += '--no-deps' }
    $args += $wheel.FullName

    python -m pip @args
    Write-Host "Installed: $($wheel.Name)"
}