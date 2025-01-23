#!/usr/bin/env python3
import json
import logging
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from modules.gui import SoundboardGUI
from modules.audio import AudioPlayer
from modules.gpio_handler import GPIOHandler
from modules.hid_communication import HIDCommunication
from modules.config_manager import ConfigManager
import sys

class Soundboard:
    def __init__(self, app):
        # QApplication Referenz speichern
        self.app = app
        
        # Logging zuerst einrichten
        self._setup_logging()
        
        # Konfiguration laden
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Audio-Player vor GUI initialisieren
        self.audio_player = AudioPlayer(self.config['audio_settings'])
        
        # GUI initialisieren
        self.gui = SoundboardGUI(self._handle_button_press, self.config)
        self.gui.set_audio_player(self.audio_player)  # Audio-Player-Referenz setzen
        
        # Andere Module nach GUI initialisieren
        self.gpio_handler = GPIOHandler(self.config['gpio_pins'], self._handle_gpio_event)
        self.hid_comm = HIDCommunication()
        
    def _setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / 'soundboard.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _handle_button_press(self, button_id):
        """Verarbeitet Touchscreen-Button-Events"""
        try:
            button_config = self.config['buttons'].get(str(button_id))
            action = button_config.get('action') if button_config else None
            if action:
                if action.endswith(('.wav', '.mp3')):
                    self.audio_player.play(action)
                else:
                    self.hid_comm.send_command(action)
        except Exception as e:
            logging.error(f"Fehler bei Button-Verarbeitung: {e}")

    def _handle_gpio_event(self, pin):
        """Verarbeitet GPIO-Button-Events"""
        try:
            action = self.config['gpio_actions'].get(str(pin))
            if action:
                if action.endswith(('.wav', '.mp3')):
                    self.audio_player.play(action)
                else:
                    self.hid_comm.send_command(action)
        except Exception as e:
            logging.error(f"Fehler bei GPIO-Verarbeitung: {e}")

    def run(self):
        """Startet die Hauptanwendung"""
        try:
            logging.info("Soundboard wird gestartet...")
            self.gui.show()
            return self.app.exec_()
        except Exception as e:
            logging.error(f"Kritischer Fehler: {e}")
            raise

def main():
    # Erstelle QApplication vor allem anderen
    app = QApplication(sys.argv)
    
    try:
        soundboard = Soundboard(app)
        return soundboard.run()
    except Exception as e:
        logging.error(f"Fataler Fehler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 