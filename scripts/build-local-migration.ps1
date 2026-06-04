param(
  [string]$LegacyWorkspaceRoot = ""
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$MigrationRoot = Join-Path $RepoRoot ".local-migration"
$SnapshotRoot = Join-Path $MigrationRoot "snapshot"
$PreservedRoot = Join-Path $MigrationRoot "_preserved"

if (Test-Path -LiteralPath $SnapshotRoot) {
  if (Test-Path -LiteralPath $PreservedRoot) {
    Remove-Item -LiteralPath $PreservedRoot -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path $PreservedRoot | Out-Null
  Get-ChildItem -Force -LiteralPath $SnapshotRoot |
    Where-Object { $_.Name -ne "codex-context-ops-repo" } |
    ForEach-Object {
      Copy-Item -LiteralPath $_.FullName -Destination $PreservedRoot -Recurse -Force
    }
  Remove-Item -LiteralPath $SnapshotRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $SnapshotRoot | Out-Null

if (Test-Path -LiteralPath $PreservedRoot) {
  Get-ChildItem -Force -LiteralPath $PreservedRoot | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $SnapshotRoot -Recurse -Force
  }
  Remove-Item -LiteralPath $PreservedRoot -Recurse -Force
}

if ($LegacyWorkspaceRoot) {
  $OutputsRoot = Join-Path ([System.IO.Path]::GetFullPath($LegacyWorkspaceRoot)) "outputs"
  if (-not (Test-Path -LiteralPath $OutputsRoot)) {
    throw "Legacy outputs directory not found: $OutputsRoot"
  }

  $Artifacts = @(
    "codex-context-governance-guide.md",
    "context-governance-kit",
    "codex-context-ops",
    "codex-context-ops-marketplace",
    "codex-context-ops-marketplace.zip",
    "codex-context-ops-repo.zip"
  )

  foreach ($Artifact in $Artifacts) {
    $Source = Join-Path $OutputsRoot $Artifact
    if (Test-Path -LiteralPath $Source) {
      Copy-Item -LiteralPath $Source -Destination $SnapshotRoot -Recurse -Force
    }
  }
}

$RepoSnapshot = Join-Path $SnapshotRoot "codex-context-ops-repo"
New-Item -ItemType Directory -Force -Path $RepoSnapshot | Out-Null

Get-ChildItem -Force -LiteralPath $RepoRoot |
  Where-Object { $_.Name -notin @(".git", ".local-migration") } |
  ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $RepoSnapshot -Recurse -Force
  }

$Index = foreach ($File in Get-ChildItem -File -Recurse -LiteralPath $SnapshotRoot | Sort-Object FullName) {
  [PSCustomObject]@{
    path = $File.FullName.Substring($SnapshotRoot.Length + 1).Replace("\", "/")
    bytes = $File.Length
    sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $File.FullName).Hash.ToLowerInvariant()
  }
}

$Index | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $MigrationRoot "file-index.json") -Encoding UTF8

$Summary = [PSCustomObject]@{
  generated_at = (Get-Date).ToString("o")
  source_repo = $RepoRoot
  file_count = @($Index).Count
  total_bytes = (@($Index) | Measure-Object -Property bytes -Sum).Sum
}

$Summary | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $MigrationRoot "snapshot-summary.json") -Encoding UTF8

Write-Host "Migration snapshot created: $MigrationRoot"
Write-Host "Files indexed: $($Summary.file_count)"
Write-Host "Total bytes: $($Summary.total_bytes)"
