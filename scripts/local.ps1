param([ValidateSet('up','down','status','test','logs')][string]$Action = 'up')
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    if ($Action -eq 'up') {
        node scripts/setup.mjs
        if ($LASTEXITCODE -ne 0) { throw 'Environment setup failed.' }
        docker compose config --quiet
        if ($LASTEXITCODE -ne 0) { throw 'Invalid Compose configuration.' }
        docker compose up --build -d --wait
    } elseif ($Action -eq 'test') {
        docker compose --profile test run --rm test
    } elseif ($Action -eq 'status') {
        docker compose ps
    } elseif ($Action -eq 'logs') {
        docker compose logs --tail 100 api worker
    } else {
        docker compose down
    }
    if ($LASTEXITCODE -ne 0) { throw ('Docker action failed: ' + $Action) }
} finally { Pop-Location }
