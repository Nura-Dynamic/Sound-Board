@echo off
title Soundboard Receiver Installation
color 0A

echo Soundboard Receiver Installation
echo ==============================
echo.

:: Prüfe Python-Installation
python --version > nul 2>&1
if errorlevel 1 (
    echo Python ist nicht installiert!
    echo Bitte installieren Sie Python von https://www.python.org/downloads/
    echo und stellen Sie sicher, dass "Add Python to PATH" aktiviert ist.
    pause
    exit /b 1
)

:: Erstelle virtuelle Umgebung
echo Erstelle virtuelle Python-Umgebung...
python -m venv venv
if errorlevel 1 (
    echo Fehler beim Erstellen der virtuellen Umgebung!
    pause
    exit /b 1
)

:: Aktiviere virtuelle Umgebung und installiere Abhängigkeiten
echo Installiere Abhängigkeiten...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Fehler beim Installieren der Abhängigkeiten!
    pause
    exit /b 1
)

:: Erstelle Verknüpfung im Startmenü
echo Erstelle Startmenü-Verknüpfung...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Soundboard Receiver.lnk'); $Shortcut.TargetPath = '%~dp0run_soundboard.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"

:: Erstelle Desktop-Verknüpfung
echo Erstelle Desktop-Verknüpfung...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Soundboard Receiver.lnk'); $Shortcut.TargetPath = '%~dp0run_soundboard.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"

:: Erstelle Ordner für Logs
if not exist logs mkdir logs

echo.
echo Installation abgeschlossen!
echo.
echo Sie können den Soundboard Receiver jetzt starten über:
echo 1. Desktop-Verknüpfung
echo 2. Startmenü
echo 3. run_soundboard.bat
echo.
echo Drücken Sie eine Taste zum Starten des Receivers...
pause > nul

:: Starte den Receiver
start run_soundboard.bat 