param(
    [string]$Target = ".",
    [ValidateSet("auto", "core", "web", "backend", "ai-data", "unity", "product-design", "marketing-cn", "review")]
    [string]$Profile = "auto",
    [string]$SourceRepo = "",
    [switch]$Force,
    [switch]$ListProfiles
)

$ErrorActionPreference = "Stop"

$Profiles = @{
    "core" = @(
        "engineering-codebase-onboarding-engineer",
        "engineering-software-architect",
        "engineering-code-reviewer",
        "engineering-minimal-change-engineer",
        "testing-test-results-analyzer",
        "engineering-technical-writer"
    )
    "web" = @(
        "engineering-codebase-onboarding-engineer",
        "engineering-software-architect",
        "engineering-code-reviewer",
        "engineering-minimal-change-engineer",
        "testing-test-results-analyzer",
        "engineering-technical-writer",
        "engineering-frontend-developer",
        "engineering-backend-architect",
        "engineering-database-optimizer",
        "testing-api-tester",
        "testing-accessibility-auditor",
        "design-ui-designer"
    )
    "backend" = @(
        "engineering-codebase-onboarding-engineer",
        "engineering-software-architect",
        "engineering-code-reviewer",
        "engineering-minimal-change-engineer",
        "testing-test-results-analyzer",
        "engineering-technical-writer",
        "engineering-backend-architect",
        "engineering-database-optimizer",
        "engineering-devops-automator",
        "engineering-sre",
        "testing-api-tester",
        "engineering-security-engineer"
    )
    "ai-data" = @(
        "engineering-codebase-onboarding-engineer",
        "engineering-software-architect",
        "engineering-code-reviewer",
        "engineering-minimal-change-engineer",
        "testing-test-results-analyzer",
        "engineering-technical-writer",
        "engineering-ai-engineer",
        "engineering-data-engineer",
        "engineering-ai-data-remediation-engineer",
        "specialized-model-qa",
        "testing-evidence-collector"
    )
    "unity" = @(
        "engineering-codebase-onboarding-engineer",
        "engineering-software-architect",
        "engineering-code-reviewer",
        "engineering-minimal-change-engineer",
        "testing-test-results-analyzer",
        "engineering-technical-writer",
        "unity-architect",
        "unity-editor-tool-developer",
        "unity-shader-graph-artist",
        "game-designer",
        "technical-artist",
        "testing-reality-checker"
    )
    "product-design" = @(
        "product-manager",
        "product-feedback-synthesizer",
        "product-sprint-prioritizer",
        "design-ux-researcher",
        "design-ux-architect",
        "design-ui-designer",
        "project-management-project-shepherd"
    )
    "marketing-cn" = @(
        "marketing-xiaohongshu-operator",
        "marketing-douyin-strategist",
        "marketing-wechat-official-account",
        "marketing-weixin-channels-strategist",
        "marketing-bilibili-strategist",
        "marketing-china-ecommerce-operator",
        "marketing-private-domain-operator"
    )
    "review" = @(
        "engineering-code-reviewer",
        "engineering-security-engineer",
        "testing-api-tester",
        "testing-performance-benchmarker",
        "testing-accessibility-auditor",
        "testing-test-results-analyzer",
        "compliance-auditor"
    )
}

function Write-Info($Message) {
    Write-Host "[agency-agents] $Message"
}

function Resolve-Target($Path) {
    $resolved = Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue
    if ($resolved) {
        return $resolved.Path
    }
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
    return (Resolve-Path -LiteralPath $Path).Path
}

function Infer-Profile($Root) {
    if ((Test-Path (Join-Path $Root "ProjectSettings\ProjectVersion.txt")) -or (Test-Path (Join-Path $Root "Assets"))) {
        return "unity"
    }
    if ((Test-Path (Join-Path $Root "package.json")) -or (Test-Path (Join-Path $Root "vite.config.*")) -or (Test-Path (Join-Path $Root "next.config.*"))) {
        return "web"
    }
    if ((Test-Path (Join-Path $Root "pyproject.toml")) -or (Test-Path (Join-Path $Root "requirements.txt")) -or (Test-Path (Join-Path $Root "notebooks"))) {
        return "ai-data"
    }
    if ((Test-Path (Join-Path $Root "docker-compose.yml")) -or (Test-Path (Join-Path $Root "Dockerfile")) -or (Test-Path (Join-Path $Root "go.mod")) -or (Test-Path (Join-Path $Root "pom.xml"))) {
        return "backend"
    }
    return "core"
}

if ($ListProfiles) {
    $Profiles.Keys | Sort-Object | ForEach-Object {
        Write-Host "$_ : $($Profiles[$_] -join ', ')"
    }
    exit 0
}

$TargetRoot = Resolve-Target $Target
if ($Profile -eq "auto") {
    $Profile = Infer-Profile $TargetRoot
    Write-Info "auto profile selected: $Profile"
}

if (-not $Profiles.ContainsKey($Profile)) {
    throw "Unknown profile: $Profile"
}

if ([string]::IsNullOrWhiteSpace($SourceRepo)) {
    $SourceRepo = Join-Path $env:TEMP "agency-agents-zh"
}

if (Test-Path (Join-Path $SourceRepo ".git")) {
    Write-Info "updating source repo: $SourceRepo"
    git -C $SourceRepo pull --ff-only | Out-Host
} else {
    if (Test-Path $SourceRepo) {
        throw "SourceRepo exists but is not a git repo: $SourceRepo"
    }
    Write-Info "cloning agency-agents-zh to: $SourceRepo"
    git clone --depth 1 https://github.com/jnMetaCode/agency-agents-zh.git $SourceRepo | Out-Host
}

$ConvertScript = Join-Path $SourceRepo "scripts\convert.ps1"
if (-not (Test-Path $ConvertScript)) {
    throw "Missing convert script: $ConvertScript"
}

Write-Info "converting agents for Codex"
powershell -NoProfile -ExecutionPolicy Bypass -File $ConvertScript -Tool codex | Out-Host

$SourceAgents = Join-Path $SourceRepo "integrations\codex\agents"
if (-not (Test-Path $SourceAgents)) {
    throw "Missing generated Codex agents: $SourceAgents"
}

$DestAgents = Join-Path $TargetRoot ".codex\agents"
New-Item -ItemType Directory -Force -Path $DestAgents | Out-Null

$Installed = @()
$Skipped = @()
$Missing = @()

foreach ($Agent in $Profiles[$Profile]) {
    $src = Join-Path $SourceAgents "$Agent.toml"
    $dst = Join-Path $DestAgents "$Agent.toml"
    if (-not (Test-Path $src)) {
        $Missing += $Agent
        continue
    }
    if ((Test-Path $dst) -and (-not $Force)) {
        $Skipped += $Agent
        continue
    }
    Copy-Item -LiteralPath $src -Destination $dst -Force:$Force
    $Installed += $Agent
}

Write-Info "target: $TargetRoot"
Write-Info "profile: $Profile"
Write-Info "agents dir: $DestAgents"
Write-Info "installed: $($Installed.Count)"
if ($Installed.Count -gt 0) {
    $Installed | ForEach-Object { Write-Host "  + $_" }
}
if ($Skipped.Count -gt 0) {
    Write-Info "skipped existing: $($Skipped.Count)"
    $Skipped | ForEach-Object { Write-Host "  = $_" }
}
if ($Missing.Count -gt 0) {
    Write-Info "missing in source: $($Missing.Count)"
    $Missing | ForEach-Object { Write-Host "  ! $_" }
}

Write-Info "restart Codex or open a new thread in this project to load new agents."
