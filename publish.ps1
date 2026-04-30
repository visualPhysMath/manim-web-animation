param(
    [string]$RepoName = "manim-web-animation",
    [ValidateSet("public", "private")]
    [string]$Visibility = "public"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI is not installed or not available in PATH."
}

gh auth status | Out-Null

$remoteNames = git remote
if ($remoteNames -contains "origin") {
    $existingRemote = git remote get-url origin
    Write-Host "Using existing origin remote: $existingRemote"
    git push -u origin main
    exit 0
}

gh repo create $RepoName --source . --remote origin --push --$Visibility

Write-Host ""
Write-Host "Repository published."
Write-Host "Open the repository Settings -> Pages and confirm Source is set to GitHub Actions."
