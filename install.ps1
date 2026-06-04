param(
  [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marketplace = Join-Path $Root "marketplace.json"
$Plugin = "codex-context-ops"
$MarketplaceName = "context-tools"

if (-not (Test-Path -LiteralPath $Marketplace)) {
  throw "marketplace.json not found next to install.ps1"
}

Write-Host "Codex Context Ops installer"
Write-Host "Marketplace: $Marketplace"

$codexCommand = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codexCommand) {
  Write-Host ""
  Write-Host "Codex CLI was not found on PATH."
  Write-Host "Open Codex app > Plugins, add this marketplace directory, then install '$Plugin'."
  Write-Host "Marketplace directory: $Root"
  exit 0
}

if ($SkipInstall) {
  Write-Host "SkipInstall set. Marketplace package is ready at: $Root"
  exit 0
}

try {
  Write-Host "Registering marketplace..."
  & codex plugin marketplace add $Root

  Write-Host "Installing plugin..."
  & codex plugin add "$Plugin@$MarketplaceName"

  Write-Host ""
  Write-Host "Installed $Plugin."
  Write-Host "Restart Codex or open a new thread, then try:"
  Write-Host '  Use $context-init to initialize this project.'
}
catch {
  Write-Host ""
  Write-Host "Automatic install did not complete:"
  Write-Host $_.Exception.Message
  Write-Host ""
  Write-Host "Manual fallback:"
  Write-Host "1. Open Codex app > Plugins."
  Write-Host "2. Add marketplace directory:"
  Write-Host "   $Root"
  Write-Host "3. Install '$Plugin' from marketplace '$MarketplaceName'."
  exit 1
}
