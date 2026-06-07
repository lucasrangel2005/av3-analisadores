param()

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

& (Join-Path $PSScriptRoot "build.ps1")

Write-Host ""
Write-Host "Teste 1: programa valido"
& (Join-Path $PSScriptRoot "run.ps1") (Join-Path $ProjectRoot "input.txt")
if ($LASTEXITCODE -ne 0) {
    throw "O programa valido falhou."
}

Write-Host ""
Write-Host "Teste 2: programa com erros semanticos esperados"
& (Join-Path $PSScriptRoot "run.ps1") (Join-Path $ProjectRoot "examples\input_semantic_error.txt")
if ($LASTEXITCODE -eq 0) {
    throw "O programa semanticamente invalido deveria falhar."
}

Write-Host ""
Write-Host "Testes concluidos: a entrada valida passa e a entrada invalida gera erros."

# Ambos os casos se comportaram como esperado; o codigo de saida do ultimo
# comando (run.ps1 do caso invalido) e 1 de proposito, entao forcamos 0 aqui
# para sinalizar que a suite de testes passou.
exit 0
