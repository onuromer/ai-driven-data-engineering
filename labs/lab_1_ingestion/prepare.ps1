# Lab 1 — Prepare: Copy Lab 0 solutions to your project
# Usage: .\labs\lab_1_ingestion\prepare.ps1 -ProjectDir ~\my-pokedex-project

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectDir
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Write-Host "==> Preparing Lab 1: Copying Lab 0 solutions to $ProjectDir"

# Lab 0: PRD + tasks
New-Item -ItemType Directory -Force -Path "$ProjectDir\docs\prds" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\docs\tasks" | Out-Null
Copy-Item "$RepoDir\labs\lab_0_context_engineering\solutions\docs\prds\*" -Destination "$ProjectDir\docs\prds\" -Force
Copy-Item "$RepoDir\labs\lab_0_context_engineering\solutions\docs\tasks\*" -Destination "$ProjectDir\docs\tasks\" -Force

Write-Host "    Lab 0 solutions copied (PRD + tasks)"
Write-Host ""
Write-Host "==> Ready for Lab 1!"
Write-Host "    Follow the instructions in labs\lab_1_ingestion\README.md"
