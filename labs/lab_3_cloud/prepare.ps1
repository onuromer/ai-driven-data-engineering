# Lab 3 — Prepare: Copy Lab 0 + Lab 1 + Lab 2 solutions and ensure DuckDB has data
# Usage: .\labs\lab_3_cloud\prepare.ps1 -ProjectDir ~\my-pokedex-project

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectDir
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Write-Host "==> Preparing Lab 3: Copying Lab 0 + Lab 1 + Lab 2 solutions to $ProjectDir"

# Lab 0: PRD + tasks
New-Item -ItemType Directory -Force -Path "$ProjectDir\docs\prds" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\docs\tasks" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\docs\learnings" | Out-Null
Copy-Item "$RepoDir\labs\lab_0_context_engineering\solutions\docs\prds\*" -Destination "$ProjectDir\docs\prds\" -Force
Copy-Item "$RepoDir\labs\lab_0_context_engineering\solutions\docs\tasks\*" -Destination "$ProjectDir\docs\tasks\" -Force
Write-Host "    Lab 0 solutions copied (PRD + tasks)"

# Lab 1: Ingestion pipeline + tests + learnings
New-Item -ItemType Directory -Force -Path "$ProjectDir\ingestion" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\tests" | Out-Null
Copy-Item "$RepoDir\labs\lab_1_ingestion\solutions\ingestion\*" -Destination "$ProjectDir\ingestion\" -Force
Copy-Item "$RepoDir\labs\lab_1_ingestion\solutions\tests\*" -Destination "$ProjectDir\tests\" -Force
Copy-Item "$RepoDir\labs\lab_1_ingestion\solutions\docs\learnings\*" -Destination "$ProjectDir\docs\learnings\" -Force
Write-Host "    Lab 1 solutions copied (ingestion pipeline + tests + learnings)"

# Lab 2: dbt project + tests + learnings
Copy-Item "$RepoDir\labs\lab_2_transformation\solutions\transform" -Destination "$ProjectDir\" -Recurse -Force
Copy-Item "$RepoDir\labs\lab_2_transformation\solutions\tests\test_transform.py" -Destination "$ProjectDir\tests\" -Force
Copy-Item "$RepoDir\labs\lab_2_transformation\solutions\docs\learnings\*" -Destination "$ProjectDir\docs\learnings\" -Force
Write-Host "    Lab 2 solutions copied (dbt project + tests + learnings)"

# Run pipeline if DuckDB doesn't exist
if (-not (Test-Path "$ProjectDir\data\pokedex.db")) {
    Write-Host ""
    Write-Host "==> DuckDB database not found. Running ingestion pipeline..."
    Write-Host "    This will fetch data from PokeAPI (may take a few minutes)"
    Push-Location $ProjectDir
    uv run python ingestion/pipeline.py
    Pop-Location
    Write-Host "    Pipeline complete!"
} else {
    Write-Host "    DuckDB database already exists at data\pokedex.db"
}

Write-Host ""
Write-Host "==> Ready for Lab 3!"
Write-Host "    Follow the instructions in labs\lab_3_cloud\README.md"
