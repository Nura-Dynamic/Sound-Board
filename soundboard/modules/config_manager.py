import json
import logging
from pathlib import Path

class ConfigManager:
    DEFAULT_CONFIG = {
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

    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        
    def load_config(self):
        """Lädt die Konfiguration aus der JSON-Datei"""
        try:
            if not self.config_path.exists():
                self._create_default_config()
                
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logging.info("Konfiguration erfolgreich geladen")
                return config
                
        except Exception as e:
            logging.error(f"Fehler beim Laden der Konfiguration: {e}")
            logging.info("Verwende Standard-Konfiguration")
            return self.DEFAULT_CONFIG

    def _create_default_config(self):
        """Erstellt eine Standard-Konfigurationsdatei"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.DEFAULT_CONFIG, f, indent=4)
            logging.info("Standard-Konfiguration erstellt")
        except Exception as e:
            logging.error(f"Fehler beim Erstellen der Standard-Konfiguration: {e}")

    def save_config(self, config):
        """Speichert die Konfiguration in die JSON-Datei"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
            logging.info("Konfiguration erfolgreich gespeichert")
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Konfiguration: {e}") 