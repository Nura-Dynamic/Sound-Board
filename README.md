# Raspberry Pi Soundboard

Ein konfigurierbares Soundboard für den Raspberry Pi mit 10-Zoll Touchscreen und GPIO-Tasten.

## Features

- 4x4 Touch-Button-Grid für Soundeffekte und Befehle
- GPIO-Unterstützung für physische Tasten
- USB HID-Kommunikation mit Windows PC
- Konfigurierbare Audio-Wiedergabe
- Logging-System für Fehlerdiagnose

## Installation

### 1. System-Abhängigkeiten installieren

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-pyqt5 \
    python3-gpiozero \
    python3-pygame \
    git
```

### 2. Repository klonen

```bash
git clone https://github.com/Nura-Dynamic/raspberry-soundboard.git
cd raspberry-soundboard
```

### 3. Python-Abhängigkeiten installieren

```bash
python3 -m pip install --user -r requirements.txt
```

### 4. Berechtigungen einrichten

```bash
# Für USB-HID Zugriff
sudo usermod -a -G plugdev $USER

# Für Audio-Zugriff
sudo usermod -a -G audio $USER
```

### 5. Konfigurationsdatei anpassen:
- Öffnen Sie `config.json` und passen Sie die Einstellungen an
- Legen Sie Ihre Sounddateien im Ordner `sounds/` ab

## Projektstruktur

```
soundboard/
├── main.py              # Hauptanwendung
├── config.json          # Konfigurationsdatei
├── requirements.txt     # Python-Abhängigkeiten
├── sounds/             # Verzeichnis für Audiodateien
│   ├── sound1.wav
│   └── sound2.wav
├── logs/               # Log-Dateien
└── modules/
    ├── __init__.py
    ├── audio.py        # Audio-Wiedergabe
    ├── config_manager.py
    ├── gpio_handler.py  # GPIO-Steuerung
    ├── gui.py          # Benutzeroberfläche
    └── hid_communication.py  # USB-Kommunikation
```

## Verwendung

### Starten des Soundboards

```bash
cd raspberry-soundboard
python3 main.py
```

### Automatischer Start beim Systemstart

Fügen Sie folgenden Eintrag zu `/etc/rc.local` hinzu (vor `exit 0`):

```bash
su pi -c 'cd /home/pi/raspberry-soundboard && python3 main.py &'
```

### Bedienung:
- Tippen Sie auf die Buttons am Touchscreen
- Verwenden Sie die konfigurierten GPIO-Tasten
- Sounds werden abgespielt oder Befehle an den PC gesendet

## Konfiguration

Die `config.json` Datei enthält alle Einstellungen:

```json
{
    "buttons": {
        "0": "sound1.wav",
        "1": "sound2.wav"
    },
    "gpio_pins": [17, 27],
    "gpio_actions": {
        "17": "play_pause",
        "27": "volume_up"
    },
    "audio_settings": {
        "output_device": "default",
        "volume": 1.0
    }
}
```

## Anforderungen

- Raspberry Pi 5
- 10-Zoll Touchscreen
- Raspberry Pi OS
- Python 3.7+
- PyQt5
- GPIO-Tasten (optional)

## Fehlersuche

### Log-Dateien prüfen
- Prüfen Sie die Logs im `logs/` Verzeichnis
```bash
tail -f logs/soundboard.log
```

### Berechtigungen
- Stellen Sie sicher, dass alle Berechtigungen korrekt gesetzt sind
```bash
ls -l /dev/snd/  # Audio-Berechtigungen
ls -l /dev/bus/usb/  # USB-Berechtigungen
```

### Audio-Test
```bash
# Test der Audio-Ausgabe
speaker-test -t wav -c 2
```

### GPIO-Test
```bash
# GPIO-Pins anzeigen
gpio readall
```

- Überprüfen Sie die Audio- und USB-Verbindungen

## Lizenz

MIT License
