@echo off
REM Script para ejecutar pruebas unitarias en Windows
REM Este script limpia las conexiones y ejecuta el runner personalizado

cd /d "%~dp0"
echo.
echo ======================================================================
echo EJECUTOR DE PRUEBAS UNITARIAS - STOCK MASTER
echo ======================================================================
echo.

REM Verificar si Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Ejecutar el script de tests
python run_tests_simple.py

pause
