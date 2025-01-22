#!/usr/bin/env python3
import json
import logging
import os
from pathlib import Path
from modules.gui import SoundboardGUI
from modules.audio import AudioPlayer
from modules.gpio_handler import GPIOHandler
from modules.hid_communication import HIDCommunication
from modules.config_manager import ConfigManager

class Soundboard:
    def __init__(self):
        # Logging einrichten
        self._setup_logging()
        
        # Konfiguration laden
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Module initialisieren
        self.audio_player = AudioPlayer(self.config['audio_settings'])
        self.gpio_handler = GPIOHandler(self.config['gpio_pins'], self._handle_gpio_event)
        self.hid_comm = HIDCommunication()
        
        # GUI als letztes initialisieren
        self.gui = SoundboardGUI(self._handle_button_press)
        
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
            action = self.config['buttons'].get(str(button_id))
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
            self.gui.run()
        except Exception as e:
            logging.error(f"Kritischer Fehler: {e}")
            raise

if __name__ == "__main__":
    soundboard = Soundboard()
    soundboard.run() 