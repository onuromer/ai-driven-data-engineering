# Lab 4b — Prepare: Copy Lab 0-3 solutions and ensure DuckDB has data
# Usage: .\labs\lab_4b_visualization\prepare.ps1 -ProjectDir ~\my-pokedex-project

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectDir
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)

# Run Lab 3 prepare first (includes Labs 0-2)
& "$RepoDir\labs\lab_3_cloud\prepare.ps1" -ProjectDir $ProjectDir

Write-Host ""
Write-Host "==> Preparing Lab 4b: Copying Lab 3 solutions to $ProjectDir"

# Lab 3: Terraform + adapted pipeline + dbt config + learnings + .env.example
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\infra" -Destination "$ProjectDir\" -Recurse -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\ingestion\pipeline.py" -Destination "$ProjectDir\ingestion\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\transform\*" -Destination "$ProjectDir\transform\" -Recurse -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\docs\prds\*" -Destination "$ProjectDir\docs\prds\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\docs\tasks\*" -Destination "$ProjectDir\docs\tasks\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\.env.example" -Destination "$ProjectDir\" -Force
if (Test-Path "$RepoDir\labs\lab_3_cloud\solutions\docs\learnings") {
    Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\docs\learnings\*" -Destination "$ProjectDir\docs\learnings\" -Force
}
Write-Host "    Lab 3 solutions copied (Terraform + pipeline + dbt + .env.example + learnings)"

Write-Host ""
Write-Host "==> Ready for Lab 4b!"
Write-Host "    Follow the instructions in labs\lab_4b_visualization\README.md"
