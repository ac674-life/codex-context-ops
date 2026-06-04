param(
  [Parameter(Mandatory = $true)]
  [string]$Destination
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$MigrationRoot = Join-Path $RepoRoot ".local-migration"
$SnapshotRoot = Join-Path $MigrationRoot "snapshot"

if (-not (Test-Path -LiteralPath $SnapshotRoot)) {
  throw "Migration snapshot not found: $SnapshotRoot"
}

$DestinationPath = [System.IO.Path]::GetFullPath($Destination)
New-Item -ItemType Directory -Force -Path $DestinationPath | Out-Null

Get-ChildItem -Force -LiteralPath $SnapshotRoot | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination $DestinationPath -Recurse -Force
}

Write-Host "Migration snapshot restored to: $DestinationPath"
