import os
import sys
import winreg
import subprocess
from pathlib import Path

def install_service():
    try:
        # Pfad zum aktuellen Verzeichnis
        current_dir = Path(__file__).parent.absolute()
        python_exe = sys.executable
        script_path = current_dir / "soundboard_receiver.py"
        
        # Erstelle .bat Datei für den Service
        bat_path = current_dir / "run_soundboard.bat"
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\n"{python_exe}" "{script_path}"\n')
        
        # NSSM (Non-Sucking Service Manager) herunterladen und installieren
        nssm_url = "https://nssm.cc/release/nssm-2.24.zip"
        subprocess.run(["powershell", "-Command", 
            f"Invoke-WebRequest {nssm_url} -OutFile nssm.zip"])
        subprocess.run(["powershell", "-Command", 
            "Expand-Archive nssm.zip -DestinationPath ."])
        
        # Service installieren
        nssm_exe = current_dir / "nssm-2.24/win64/nssm.exe"
        subprocess.run([
            str(nssm_exe), "install", "SoundboardReceiver",
            str(bat_path)
        ])
        
        # Service konfigurieren
        subprocess.run([str(nssm_exe), "set", "SoundboardReceiver", 
            "DisplayName", "Soundboard HID Receiver"])
        subprocess.run([str(nssm_exe), "set", "SoundboardReceiver", 
            "Description", "Empfängt und verarbeitet HID-Befehle vom Soundboard"])
        
        # Service starten
        subprocess.run(["net", "start", "SoundboardReceiver"])
        
        print("Service erfolgreich installiert und gestartet!")
        print("Der Soundboard Receiver startet nun automatisch mit Windows.")
        
    except Exception as e:
        print(f"Fehler bei der Installation: {e}")
        return False
    
    return True

def add_to_startup():
    try:
        # Füge Verknüpfung zum Autostart-Ordner hinzu
        startup_folder = os.path.join(
            os.getenv('APPDATA'),
            r'Microsoft\Windows\Start Menu\Programs\Startup'
        )
        
        current_dir = Path(__file__).parent.absolute()
        bat_path = current_dir / "run_soundboard.bat"
        
        # Erstelle .vbs Datei für verstecktes Fenster
        vbs_path = current_dir / "start_hidden.vbs"
        with open(vbs_path, 'w') as f:
            f.write(f'CreateObject("Wscript.Shell").Run "{bat_path}", 0, True')
        
        # Erstelle Verknüpfung
        shortcut_path = os.path.join(startup_folder, "Soundboard Receiver.lnk")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Run") as key:
            winreg.SetValueEx(key, "Soundboard Receiver", 0, 
                winreg.REG_SZ, str(vbs_path))
        
        print("Autostart erfolgreich eingerichtet!")
        
    except Exception as e:
        print(f"Fehler beim Einrichten des Autostarts: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if not os.path.isfile("config.json"):
        # Erstelle Standard-Konfiguration
        with open("config.json", "w") as f:
            f.write('''{
    "hid_commands": {
        "media_play_pause": [0x01],
        "media_next": [0x02],
        "media_prev": [0x03],
        "volume_up": [0x04],
        "volume_down": [0x05]
    }
}''')
    
    print("Installiere Soundboard Receiver...")
    
    # Als Administrator ausführen
    if not os.environ.get("ELEVATED"):
        if sys.platform == 'win32':
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:])
            subprocess.run(["powershell", "Start-Process", "python", 
                f"-ArgumentList '{params}'", "-Verb", "RunAs"])
            sys.exit(0)
    
    if install_service() and add_to_startup():
        print("\nInstallation abgeschlossen!")
        print("1. Der Receiver läuft jetzt als Windows-Dienst")
        print("2. Der Dienst startet automatisch mit Windows")
        print("3. Prüfen Sie die Logs unter 'logs/receiver.log'")
        input("\nDrücken Sie Enter zum Beenden...")
    else:
        print("\nInstallation fehlgeschlagen!")
        print("Bitte prüfen Sie die Berechtigungen und versuchen Sie es erneut.")
        input("\nDrücken Sie Enter zum Beenden...") 