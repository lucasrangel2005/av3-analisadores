param()

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$LibDir = Join-Path $ProjectRoot "lib"
$ToolDir = Join-Path $ProjectRoot "build\tools"

New-Item -ItemType Directory -Force -Path $LibDir, $ToolDir | Out-Null

function Download-File {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (Test-Path $Destination) {
        return
    }

    Write-Host "Baixando $Url"
    Invoke-WebRequest -Uri $Url -OutFile $Destination -UseBasicParsing
}

$JFlexZip = Join-Path $LibDir "jflex-1.9.1.zip"
$CupJar = Join-Path $LibDir "java-cup-11b-20160615-3.jar"
$CupRuntimeJar = Join-Path $LibDir "java-cup-runtime-11b-20160615-3.jar"
$EcjJar = Join-Path $LibDir "ecj-4.6.1.jar"

Download-File "https://github.com/jflex-de/jflex/releases/download/v1.9.1/jflex-1.9.1.zip" $JFlexZip
Download-File "https://repo1.maven.org/maven2/com/github/vbmacher/java-cup/11b-20160615-3/java-cup-11b-20160615-3.jar" $CupJar
Download-File "https://repo1.maven.org/maven2/com/github/vbmacher/java-cup-runtime/11b-20160615-3/java-cup-runtime-11b-20160615-3.jar" $CupRuntimeJar
Download-File "https://repo1.maven.org/maven2/org/eclipse/jdt/core/compiler/ecj/4.6.1/ecj-4.6.1.jar" $EcjJar

$JFlexJar = Join-Path $LibDir "jflex-full-1.9.1.jar"
if (-not (Test-Path $JFlexJar)) {
    $ExtractDir = Join-Path $ToolDir "jflex-1.9.1"
    if (Test-Path $ExtractDir) {
        Remove-Item -LiteralPath $ExtractDir -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $ExtractDir | Out-Null
    Expand-Archive -LiteralPath $JFlexZip -DestinationPath $ExtractDir -Force

    $Candidate = Get-ChildItem -Path $ExtractDir -Recurse -Filter "jflex-full-*.jar" | Select-Object -First 1
    if ($null -eq $Candidate) {
        $Candidate = Get-ChildItem -Path $ExtractDir -Recurse -Filter "jflex-*.jar" | Select-Object -First 1
    }
    if ($null -eq $Candidate) {
        throw "Nao foi encontrado um JAR do JFlex dentro de $JFlexZip."
    }
    Copy-Item -LiteralPath $Candidate.FullName -Destination $JFlexJar -Force
    Remove-Item -LiteralPath $ExtractDir -Recurse -Force
}

Write-Host "Ferramentas disponiveis em $LibDir"
