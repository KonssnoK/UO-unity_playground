# Full-binary Ghidra dump: decompile every function in UOSA.exe, write JSONL.
# Re-uses the existing imported project (so no re-analysis cost on rerun).
$ErrorActionPreference = 'Stop'

$root      = Resolve-Path "$PSScriptRoot"
$jdkHome   = Join-Path $root 'jdk\jdk-21.0.11+10'
$ghidra    = Join-Path $root 'ghidra_12.1_PUBLIC'
$project   = Join-Path $root 'project'
$postdir   = Join-Path $root 'scripts'
$exe       = 'C:\Games\Electronic Arts\Ultima Online Enhanced\UOSA.exe'

$env:JAVA_HOME = $jdkHome
$env:PATH      = "$jdkHome\bin;" + $env:PATH
$env:GHIDRA_OUT_JSONL  = Join-Path $root 'ghidra_full.jsonl'
$env:GHIDRA_OUT_INDEX  = Join-Path $root 'ghidra_full_index.json'
$env:GHIDRA_HEADLESS_MAXMEM = '24G'

$bat = Join-Path $ghidra 'support\analyzeHeadless.bat'
$projName = 'UOSA_proj'
$gpr = Join-Path $project "$projName.gpr"

Write-Host "JAVA_HOME = $env:JAVA_HOME"
Write-Host "Project   = $project"
Write-Host "Out JSONL = $env:GHIDRA_OUT_JSONL"
Write-Host "Out INDEX = $env:GHIDRA_OUT_INDEX"
Write-Host ""

if (Test-Path $gpr) {
    Write-Host "Re-opening existing project (auto-analysis cached) -> $gpr"
    & $bat $project $projName `
        -process UOSA.exe `
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
