# Install Liniya Sporta Design Studio skills and subagents for local Codex.
# Run this PowerShell script from your cloned ls-docs directory.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$skillsSource = Join-Path $root '.agents\skills'
$agentsSource = Join-Path $root '.codex\agents'
$skillsTarget = Join-Path $HOME '.agents\skills'
$agentsTarget = Join-Path $HOME '.codex\agents'
New-Item -ItemType Directory -Path $skillsTarget, $agentsTarget -Force | Out-Null

foreach ($item in (Get-ChildItem -LiteralPath $skillsSource -Directory -Filter 'ls-*')) {
    $dest = Join-Path $skillsTarget $item.Name
    if (Test-Path -LiteralPath $dest) {
        Write-Warning "Already installed; keeping existing skill: $dest"
    } else {
        Copy-Item -LiteralPath $item.FullName -Destination $dest -Recurse
        Write-Host "Installed skill: $($item.Name)"
    }
}
foreach ($item in (Get-ChildItem -LiteralPath $agentsSource -File -Filter 'ls_*.toml')) {
    $dest = Join-Path $agentsTarget $item.Name
    if (Test-Path -LiteralPath $dest) {
        Write-Warning "Already installed; keeping existing agent: $dest"
    } else {
        Copy-Item -LiteralPath $item.FullName -Destination $dest
        Write-Host "Installed subagent: $($item.Name)"
    }
}
Write-Host 'Restart Codex, then use /skills. ChatGPT web plugin installation is separate.'
