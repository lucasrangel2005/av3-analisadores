param()

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$LibDir = Join-Path $ProjectRoot "lib"
$GeneratedDir = Join-Path $ProjectRoot "src\generated\java"
$ParserDir = Join-Path $GeneratedDir "br\edu\compiladores\parser"
$LexerDir = Join-Path $GeneratedDir "br\edu\compiladores\lexer"

& (Join-Path $PSScriptRoot "download-tools.ps1")

if (Test-Path $GeneratedDir) {
    Remove-Item -LiteralPath $GeneratedDir -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $ParserDir, $LexerDir | Out-Null

$CupJar = Join-Path $LibDir "java-cup-11b-20160615-3.jar"
$JFlexJar = Join-Path $LibDir "jflex-full-1.9.1.jar"
$CupSpec = Join-Path $ProjectRoot "src\main\cup\MiniLang.cup"
$FlexSpec = Join-Path $ProjectRoot "src\main\jflex\MiniLang.flex"

Write-Host "Gerando Parser.java e sym.java com JCup..."
& java -cp $CupJar java_cup.Main -parser Parser -symbols sym -destdir $ParserDir $CupSpec
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao gerar arquivos do JCup."
}

Write-Host "Gerando Scanner.java com JFlex..."
& java -jar $JFlexJar -d $LexerDir $FlexSpec
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao gerar arquivo do JFlex."
}

Write-Host "Arquivos gerados em $GeneratedDir"
