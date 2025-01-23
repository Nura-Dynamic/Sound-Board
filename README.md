# Raspberry Pi Soundboard

Ein modernes Soundboard für den Raspberry Pi mit 10-Zoll Touchscreen, Audio-Effekten und GPIO-Steuerung.

Kann auch unter Windows als HID-Empfänger verwendet werden.

## Features

- 16 konfigurierbare Sound-Buttons
- 4-Kanal Audio-Mixer
- Echtzeit Audio-Effekte:
  - Autotune
  - Echo
  - Reverb
  - Distortion
- Touch-optimierte Benutzeroberfläche
- GPIO-Unterstützung für externe Tasten
- USB HID-Kommunikation mit Windows PC

## Systemanforderungen

- Raspberry Pi 4/5
- Raspberry Pi OS mit Desktop
- 10-Zoll Touchscreen (1280x800)
- USB-Soundkarte oder HDMI-Audio
- GPIO-Tasten (optional)

## Windows-Kompatibilität

### Windows-Treiber installieren

1. Zadig USB-Treiber herunterladen: [https://zadig.akeo.ie/](https://zadig.akeo.ie/)
2. Zadig ausführen
3. Options -> List All Devices aktivieren
4. "Soundboard HID Device" auswählen
5. WinUSB-Treiber installieren

### Windows-Client installieren

1. Python für Windows installieren von [python.org](https://www.python.org/downloads/)
2. Windows-Client herunterladen und entpacken
3. Abhängigkeiten installieren:
```cmd
cd windows_client
pip install -r requirements.txt
```

4. Client starten:
```cmd
python soundboard_receiver.py
```

Der Client läuft im Hintergrund und verarbeitet die Befehle vom Soundboard.
Er kann auch als Windows-Dienst installiert werden.

5. Als Windows-Dienst installieren (optional):
```cmd
python install_service.py
```
Dies installiert den Client als Windows-Dienst und richtet den Autostart ein.

### Windows-Konfiguration

Bearbeiten Sie die `config.json` für Windows-Befehle:

```json
{
    "buttons": {
        "4": {
            "text": "Play",
            "action": "media_play_pause",
            "type": "command"
        },
        "5": {
            "text": "Next",
            "action": "media_next",
            "type": "command"
        }
    },
    "hid_commands": {
        "media_play_pause": [0x01],
        "media_next": [0x02],
        "media_prev": [0x03],
        "volume_up": [0x04],
        "volume_down": [0x05]
    }
}
```

### Unterstützte Windows-Befehle

- Mediensteuerung:
  - play_pause
  - next_track
  - prev_track
  - volume_up
  - volume_down
  - mute
- Tastatureingaben
- Maussteuerung

## Installation

### Raspberry Pi

### 1. System-Pakete installieren

```bash
# System-Updates
sudo apt-get update
sudo apt-get upgrade

# Benötigte System-Pakete
sudo apt-get install -y \
    python3-full \
    python3-pip \
    python3-venv \
    python3-pyqt5 \
    python3-numpy \
    python3-scipy \
    python3-soundfile \
    python3-librosa \
    portaudio19-dev \
    libsndfile1 \
    libsndfile1-dev \
    libasound2-dev \
    python3-usb \
    git
```

### 2. Soundboard herunterladen

```bash
# Repository klonen
git clone https://github.com/Nura-Dynamic/Sound-Board.git
cd Sound-Board

# Virtuelle Umgebung erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate

# Abhängigkeiten installieren
python -m pip install --upgrade pip
pip install -r requirements.txt --no-deps

# Ausführbar machen
chmod +x run.sh
```

### 3. Starten

```bash
./run.sh
```

Oder manuell:
```bash
source venv/bin/activate
cd soundboard
python main.py
```

### Windows-Client installieren

1. Python für Windows installieren von [python.org](https://www.python.org/downloads/)
2. Windows-Client herunterladen und entpacken
3. Abhängigkeiten installieren:
```cmd
cd windows_client
pip install -r requirements.txt
```

4. Client starten:
```cmd
python soundboard_receiver.py
```

5. Als Windows-Dienst installieren (optional):
```cmd
python install_service.py
```

### Audio-Konfiguration

1. USB-Soundkarte anschließen
2. ALSA-Mixer öffnen:
```bash
alsamixer
```
3. Mit F6 USB-Soundkarte auswählen
4. Lautstärke einstellen

### GPIO-Konfiguration

Pins in config.json anpassen:
```json
{
  "gpio_pins": {
    "17": "button1",
    "18": "button2",
    "27": "button3",
    "22": "button4"
  }
}
```

## Fehlerbehebung

### Audio-Probleme

1. ALSA-Geräte prüfen:
```bash
aplay -l
```

2. Audio-Gruppe prüfen:
```bash
groups | grep audio
```

3. Logs prüfen:
```bash
tail -f logs/soundboard.log
```

### GUI-Probleme

1. X-Server Status:
```bash
echo $DISPLAY
```

2. Qt-Plugins prüfen:
```bash
QT_DEBUG_PLUGINS=1 python3 soundboard/main.py
```

### USB/HID-Probleme

1. USB-Geräte prüfen:
```bash
lsusb
```

2. USB-Berechtigungen:
```bash
sudo usermod -a -G plugdev $USER
```

3. Udev-Regeln erstellen:
```bash
sudo nano /etc/udev/rules.d/99-soundboard.rules
```
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5750", MODE="0666"
```
```bash
sudo udevadm control --reload-rules
```

## Lizenz

MIT License - Siehe LICENSE Datei

## Beitragen

1. Fork erstellen
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen
