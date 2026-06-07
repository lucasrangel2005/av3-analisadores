param(
    [string]$InputFile = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$LibDir = Join-Path $ProjectRoot "lib"
$ClassesDir = Join-Path $ProjectRoot "build\classes"

if ([string]::IsNullOrWhiteSpace($InputFile)) {
    $InputFile = Join-Path $ProjectRoot "input.txt"
}

if (-not (Test-Path $ClassesDir)) {
    & (Join-Path $PSScriptRoot "build.ps1")
}

$CupRuntimeJar = Join-Path $LibDir "java-cup-runtime-11b-20160615-3.jar"
$Classpath = "$ClassesDir;$CupRuntimeJar"

& java -cp $Classpath br.edu.compiladores.Main $InputFile
exit $LASTEXITCODE
