param()

$ErrorActionPreference = "Stop"

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
    & $Python.Source (Join-Path $PSScriptRoot "build-report.py")
} else {
    & py -3 (Join-Path $PSScriptRoot "build-report.py")
}
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao gerar relatorio PDF."
}
