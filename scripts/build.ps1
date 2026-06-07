param()

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$LibDir = Join-Path $ProjectRoot "lib"
$BuildDir = Join-Path $ProjectRoot "build"
$ClassesDir = Join-Path $BuildDir "classes"
$SourcesFile = Join-Path $BuildDir "sources.txt"

& (Join-Path $PSScriptRoot "generate.ps1")

if (Test-Path $ClassesDir) {
    Remove-Item -LiteralPath $ClassesDir -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $ClassesDir | Out-Null

$SourceRoots = @(
    (Join-Path $ProjectRoot "src\generated\java"),
    (Join-Path $ProjectRoot "src\main\java")
)

$Sources = Get-ChildItem -Path $SourceRoots -Recurse -Filter "*.java" | Sort-Object FullName | ForEach-Object { '"' + $_.FullName + '"' }
Set-Content -LiteralPath $SourcesFile -Value $Sources -Encoding ASCII

$CupRuntimeJar = Join-Path $LibDir "java-cup-runtime-11b-20160615-3.jar"
$EcjJar = Join-Path $LibDir "ecj-4.6.1.jar"

Write-Host "Compilando classes Java com ECJ..."
& java -jar $EcjJar -source 1.8 -target 1.8 -encoding UTF-8 -cp $CupRuntimeJar -d $ClassesDir "@$SourcesFile"
if ($LASTEXITCODE -ne 0) {
    throw "Falha na compilacao Java."
}

Write-Host "Compilacao concluida em $ClassesDir"
