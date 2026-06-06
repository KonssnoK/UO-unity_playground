# Runs Ghidra headless on UOSA.exe with our post-analysis script.
$ErrorActionPreference = 'Stop'

$root      = Resolve-Path "$PSScriptRoot"
$jdkHome   = Join-Path $root 'jdk\jdk-21.0.11+10'
$ghidra    = Join-Path $root 'ghidra_12.1_PUBLIC'
$project   = Join-Path $root 'project'
$postdir   = Join-Path $root 'scripts'
$exe       = 'C:\Games\Electronic Arts\Ultima Online Enhanced\UOSA.exe'
$outJson   = Join-Path $root 'ghidra_dump.json'

# Make sure the project dir exists
New-Item -ItemType Directory -Force -Path $project | Out-Null

# Configure environment for Ghidra
$env:JAVA_HOME = $jdkHome
$env:PATH      = "$jdkHome\bin;" + $env:PATH
$env:GHIDRA_OUT = $outJson

# Use more RAM (we have 94GB)
$env:GHIDRA_HEADLESS_MAXMEM = '16G'

$bat = Join-Path $ghidra 'support\analyzeHeadless.bat'

Write-Host "JAVA_HOME = $env:JAVA_HOME"
Write-Host "Project   = $project"
Write-Host "Binary    = $exe"
Write-Host "Out JSON  = $outJson"
Write-Host ""

# Headless run: import binary, run auto-analysis, run our post script, then delete the project entry.
$projName = 'UOSA_proj'
$gpr = Join-Path $project "$projName.gpr"

if (Test-Path $gpr) {
    Write-Host "Re-opening existing project (auto-analysis cached) -> $gpr"
    & $bat $project $projName `
        -process UOSA.exe `
        -noanalysis `
        -scriptPath $postdir `
        -postScript PostAnalysis.java
} else {
    Write-Host "Importing fresh and running auto-analysis"
    & $bat $project $projName `
        -import $exe `
        -scriptPath $postdir `
        -postScript PostAnalysis.java
}
