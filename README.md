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

### Windows (für HID-Empfang)

1. Zadig USB-Treiber installieren
2. Soundboard am USB-Port anschließen
3. Windows erkennt das Gerät als "HID-konformes Gerät"

### 1. System-Pakete installieren

```bash
# System-Updates
sudo apt-get update
sudo apt-get upgrade

# Benötigte System-Pakete
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    portaudio19-dev \
    libsndfile1 \
    libasound2-dev \
    python3-pyqt5 \
    python3-usb \
    git
```

### 2. Repository klonen

```bash
git clone https://github.com/Nura-Dynamic/Sound-Board.git
cd Sound-Board
```

### 3. Python-Umgebung einrichten

```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate

# Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Audio-Konfiguration

```bash
# ALSA-Konfiguration
sudo nano /etc/asound.conf
```

Fügen Sie folgende Zeilen ein:
```
pcm.!default {
    type hw
    card 1  # USB-Soundkarte oder HDMI
}

ctl.!default {
    type hw
    card 1
}
```

### 5. Berechtigungen einrichten

```bash
# Audio-Gruppe
sudo usermod -a -G audio $USER

# GPIO-Gruppe
sudo usermod -a -G gpio $USER

# USB-Gruppe für HID
sudo usermod -a -G plugdev $USER
```

## Konfiguration

### Sound-Dateien

1. Erstellen Sie einen `sounds` Ordner:
```bash
mkdir -p sounds
```

2. Kopieren Sie Ihre .wav oder .mp3 Dateien in den Ordner

### Button-Konfiguration

Bearbeiten Sie `config.json`:

```json
{
    "buttons": {
        "0": {
            "text": "Sound 1",
            "action": "sound1.wav",
            "type": "sound"
        },
        "1": {
            "text": "Sound 2",
            "action": "sound2.wav",
            "type": "sound"
        }
    },
    "audio_settings": {
        "output_device": "default",
        "volume": 1.0
    }
}
```

## Verwendung

### Programm starten

```bash
cd Sound-Board
source venv/bin/activate
python3 soundboard/main.py
```

### Bedienung

- **Sound-Buttons**: Tippen zum Abspielen
- **Lautstärke-Regler**: 4 unabhängige Kanäle
- **Effekt-Regler**:
  - Auto: Autotune-Intensität
  - Echo: Verzögerungszeit
  - Rev: Reverb-Raumgröße
  - Dist: Verzerrungsstärke

### Tastenkürzel

- `ESC`: Programm beenden
- `1-9`: Direkte Button-Auswahl

## Autostart einrichten

```bash
# Autostart-Verzeichnis erstellen
mkdir -p ~/.config/autostart

# Desktop-Eintrag erstellen
cat > ~/.config/autostart/soundboard.desktop << EOL
[Desktop Entry]
Type=Application
Name=Soundboard
Exec=bash -c 'cd /home/pi/Sound-Board && source venv/bin/activate && python3 soundboard/main.py'
Terminal=false
X-GNOME-Autostart-enabled=true
EOL
```

## Fehlerbehebung

### Windows-Probleme

1. Gerätemanager prüfen:
```
- Systemsteuerung -> Gerätemanager
- Unter "Human Interface Devices" nach "Soundboard" suchen
```

2. USB-Verbindung testen:
```
- Anderer USB-Port
- USB-Kabel prüfen
- Zadig neu installieren
```

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

## Lizenz

MIT License - Siehe LICENSE Datei

## Beitragen

1. Fork erstellen
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen
