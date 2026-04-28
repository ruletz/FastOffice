param(
  [string]$AppDir = "c:\Projects\OnlyOffice\app",
  [string]$Exe = "DesktopEditors.exe",
  [int]$WaitSeconds = 15
)

$ErrorActionPreference = "Stop"

function Get-DirSizeBytes([string]$Path) {
  if (-not (Test-Path $Path)) { return 0 }
  (Get-ChildItem -LiteralPath $Path -Recurse -File | Measure-Object -Property Length -Sum).Sum
}

Write-Host "== Size metrics =="
$bytes = Get-DirSizeBytes $AppDir
("{0} bytes ({1:N2} MB)" -f $bytes, ($bytes / 1MB)) | Write-Host

$exePath = Join-Path $AppDir $Exe
if (-not (Test-Path $exePath)) {
  Write-Host "Executable not found: $exePath"
  exit 1
}

Write-Host "`n== Launch + memory (rough) =="
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$p = Start-Process -FilePath $exePath -WorkingDirectory $AppDir -PassThru

Start-Sleep -Seconds 1
$sw.Stop()
Write-Host ("Started PID={0} in {1} ms" -f $p.Id, $sw.ElapsedMilliseconds)

Start-Sleep -Seconds $WaitSeconds
try {
  $proc = Get-Process -Id $p.Id -ErrorAction Stop
  Write-Host ("WorkingSet64: {0:N2} MB" -f ($proc.WorkingSet64 / 1MB))
  Write-Host ("PrivateMemorySize64: {0:N2} MB" -f ($proc.PrivateMemorySize64 / 1MB))
} catch {
  Write-Host "Process exited before sampling."
}

Write-Host "`nTip: close the app manually when done sampling."

