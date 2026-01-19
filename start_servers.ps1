# Script para ejecutar tanto el backend como el frontend en paralelo
Write-Host "Iniciando servidores..." -ForegroundColor Green


# Rutas dinámicas basadas en el directorio actual
$projectRoot = $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontendDir = Join-Path $projectRoot "frontend"

Write-Host "Iniciando backend FastAPI en puerto 8000..." -ForegroundColor Yellow
Start-Job -Name "Backend" -ScriptBlock {
    param($projectRoot, $venvPython)
    Set-Location $projectRoot
    & $venvPython -m uvicorn src.web.main:app --reload --port 8000
} -ArgumentList $projectRoot, $venvPython

Start-Sleep -Seconds 3

Write-Host "Iniciando frontend en puerto 8080..." -ForegroundColor Yellow
Start-Job -Name "Frontend" -ScriptBlock {
    param($frontendDir, $venvPython)
    Set-Location $frontendDir
    & $venvPython -m http.server 8080 --directory .
} -ArgumentList $frontendDir, $venvPython


Write-Host ""
Write-Host "Servidores iniciados:" -ForegroundColor Green
Write-Host "  - Backend (FastAPI): http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver el estado de los trabajos: Get-Job" -ForegroundColor White
Write-Host "Para ver los logs: Receive-Job -Name 'Backend' -Keep" -ForegroundColor White
Write-Host "Para detener los servidores: Stop-Job -Name 'Backend','Frontend'; Remove-Job -Name 'Backend','Frontend'" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para salir (pero los servidores seguirán ejecutándose en background)" -ForegroundColor Red

# Mantener el script activo y mostrar estado periódicamente
try {
    while ($true) {
        Start-Sleep -Seconds 10
        $jobs = Get-Job
        Write-Host "Estado de trabajos: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
        foreach ($job in $jobs) {
            Write-Host "  - $($job.Name): $($job.State)" -ForegroundColor Gray
        }
    }
}
catch {
    Write-Host "Script interrumpido. Los servidores siguen ejecutándose en background." -ForegroundColor Yellow
}