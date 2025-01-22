# Raspberry Pi Soundboard

Ein konfigurierbares Soundboard für den Raspberry Pi mit 10-Zoll Touchscreen und GPIO-Tasten.

## Systemanforderungen

- Raspberry Pi 5
- Raspberry Pi OS Lite (empfohlen) oder Ubuntu Server
- 10-Zoll Touchscreen
- GPIO-Tasten (optional)

## Vorbereitungen

### 1. Raspberry Pi OS Lite Installation

```bash
# Nach der Installation von Raspberry Pi OS Lite:

# X-Server und minimale Desktop-Umgebung
sudo apt-get install -y \
    xserver-xorg \
    x11-xserver-utils \
    xinit \
    openbox \
    lightdm

# Audio-Optimierungen
sudo nano /boot/firmware/config.txt
```

Fügen Sie folgende Zeilen zu config.txt hinzu:
```
# Audio-Optimierungen
dtparam=audio=on
audio_pwm_mode=2

# CPU-Optimierungen
force_turbo=1

# GPU-Speicher für Touchscreen
gpu_mem=128
```

### 2. Audio-Konfiguration

```bash
# ALSA und PulseAudio Installation
sudo apt-get install -y \
    alsa-utils \
    pulseaudio \
    pulseaudio-utils

# Realtime-Priorität für Audio
sudo adduser $USER audio
sudo nano /etc/security/limits.d/audio.conf
```

Fügen Sie folgende Zeilen zu audio.conf hinzu:
```
@audio   -  rtprio     95
@audio   -  memlock    unlimited
```

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
    python3-venv \
    python3-full \
    python3-pygame \
    python3-gpiozero \
    python3-usb \
    python3-dotenv \
    python3-setuptools \
    python3-wheel
```

### 2. Repository klonen

```bash
git clone https://github.com/Nura-Dynamic/Sound-Board.git
cd Sound-Board
```

### 3. Virtuelle Umgebung erstellen

```bash
# Virtuelle Umgebung mit Zugriff auf System-Pakete erstellen
python3 -m venv venv --system-site-packages

# Virtuelle Umgebung aktivieren
source venv/bin/activate
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
# Virtuelle Umgebung aktivieren
source venv/bin/activate
# Soundboard starten
python3 main.py
```

### Automatischer Start beim Systemstart

Fügen Sie folgenden Eintrag zu `/etc/rc.local` hinzu (vor `exit 0`):

```bash
su pi -c 'cd /home/pi/raspberry-soundboard && source venv/bin/activate && python3 main.py &'
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
