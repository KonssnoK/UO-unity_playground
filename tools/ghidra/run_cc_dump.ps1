# Full-binary Ghidra dump for the CLASSIC client (client.exe).
# Imports into its own project (CC_proj), auto-analyzes, then decompiles
# every function to JSONL so we can grep the static-draw-ordering logic.
$ErrorActionPreference = 'Stop'

$root      = Resolve-Path "$PSScriptRoot"
$jdkHome   = Join-Path $root 'jdk\jdk-21.0.11+10'
$ghidra    = Join-Path $root 'ghidra_12.1_PUBLIC'
$project   = Join-Path $root 'project'
$postdir   = Join-Path $root 'scripts'
$exe       = 'C:\Games\Electronic Arts\Ultima Online Classic\client.exe'

$env:JAVA_HOME = $jdkHome
$env:PATH      = "$jdkHome\bin;" + $env:PATH
$env:GHIDRA_OUT_JSONL  = Join-Path $root 'cc_full.jsonl'
$env:GHIDRA_OUT_INDEX  = Join-Path $root 'cc_full_index.json'
$env:GHIDRA_HEADLESS_MAXMEM = '24G'

$bat = Join-Path $ghidra 'support\analyzeHeadless.bat'
$projName = 'CC_proj'
$gpr = Join-Path $project "$projName.gpr"

Write-Host "JAVA_HOME = $env:JAVA_HOME"
Write-Host "Project   = $project\$projName"
Write-Host "Binary    = $exe"
Write-Host "Out JSONL = $env:GHIDRA_OUT_JSONL"
Write-Host ""

if (Test-Path $gpr) {
    Write-Host "Re-opening existing project (auto-analysis cached) -> $gpr"
    & $bat $project $projName `
        -process client.exe `
        -noanalysis `
        -scriptPath $postdir `
        -postScript FullDump.java
} else {
    Write-Host "Importing fresh + auto-analysis (one-time cost)"
    & $bat $project $projName `
        -import $exe `
        -scriptPath $postdir `
        -postScript FullDump.java
}
