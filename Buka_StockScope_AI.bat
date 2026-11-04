@echo off
title StockScope AI - Microstock Trend Analysis
cd /d "%~dp0"
echo ========================================================
echo   StockScope AI - Microstock Trend & Gap Analysis Tool
echo ========================================================
echo.
echo Menjalankan aplikasi StockScope AI...
echo Browser akan terbuka otomatis di http://localhost:5055
echo.
python app.py
pause
