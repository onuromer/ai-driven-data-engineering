# Lab 4c — Prepare: Copy Lab 0-3 solutions and ensure DuckDB has data
# Usage: .\labs\lab_4c_ai_ml\prepare.ps1 -ProjectDir ~\my-pokedex-project

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
Write-Host "==> Preparing Lab 4c: Copying Lab 3 solutions to $ProjectDir"

# Lab 3: Terraform + adapted pipeline + dbt profiles + learnings
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\infra" -Destination "$ProjectDir\" -Recurse -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\ingestion\pipeline.py" -Destination "$ProjectDir\ingestion\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\transform\profiles.yml" -Destination "$ProjectDir\transform\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\transform\macros\generate_schema_name.sql" -Destination "$ProjectDir\transform\macros\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\transform\models\staging\*" -Destination "$ProjectDir\transform\models\staging\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\transform\models\marts\*" -Destination "$ProjectDir\transform\models\marts\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\docs\prds\*" -Destination "$ProjectDir\docs\prds\" -Force
Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\docs\tasks\*" -Destination "$ProjectDir\docs\tasks\" -Force
if (Test-Path "$RepoDir\labs\lab_3_cloud\solutions\docs\learnings") {
    Copy-Item "$RepoDir\labs\lab_3_cloud\solutions\docs\learnings\*" -Destination "$ProjectDir\docs\learnings\" -Force
}
Write-Host "    Lab 3 solutions copied (Terraform + adapted pipeline + dbt BigQuery config + learnings)"

Write-Host ""
Write-Host "==> Ready for Lab 4c!"
Write-Host "    Follow the instructions in labs\lab_4c_ai_ml\README.md"
