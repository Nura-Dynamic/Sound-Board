@echo off
title Soundboard Receiver Deinstallation
color 0C

echo Soundboard Receiver Deinstallation
echo ================================
echo.

:: Beende laufende Instanz
taskkill /f /im python.exe /fi "WINDOWTITLE eq Soundboard Receiver" > nul 2>&1

:: Entferne Verknüpfungen
echo Entferne Verknüpfungen...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Soundboard Receiver.lnk" > nul 2>&1
del "%USERPROFILE%\Desktop\Soundboard Receiver.lnk" > nul 2>&1

:: Lösche virtuelle Umgebung
echo Entferne virtuelle Umgebung...
rmdir /s /q venv > nul 2>&1

:: Lösche Logs (optional)
choice /c yn /m "Möchten Sie auch die Log-Dateien löschen?"
if errorlevel 2 goto :skip_logs
echo Entferne Log-Dateien...
rmdir /s /q logs > nul 2>&1
:skip_logs

echo.
echo Deinstallation abgeschlossen!
echo Die Konfigurationsdatei (config.json) wurde beibehalten.
echo.
pause 