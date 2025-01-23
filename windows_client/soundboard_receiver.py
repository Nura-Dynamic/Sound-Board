import hid
import keyboard
import logging
from pathlib import Path
import json
import time

class SoundboardReceiver:
    def __init__(self):
        # Soundboard USB IDs
        self.VENDOR_ID = 0x0483
        self.PRODUCT_ID = 0x5750
        
        self.setup_logging()
        self.load_config()
        self.connect_device()

    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / 'receiver.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
            logging.info("Konfiguration geladen")
        except Exception as e:
            logging.error(f"Fehler beim Laden der Konfiguration: {e}")
            self.config = {}

    def connect_device(self):
        try:
            self.device = hid.device()
            self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
            self.device.set_nonblocking(True)
            
            logging.info("Soundboard verbunden")
            print("Soundboard erfolgreich verbunden!")
            print("Warte auf Befehle...")
            
        except Exception as e:
            logging.error(f"Verbindungsfehler: {e}")
            print("Konnte Soundboard nicht finden!")
            print("Bitte überprüfen Sie die Verbindung und Treiber")
            exit(1)

    def handle_command(self, data):
        try:
            command = data[0]
            
            # Mediensteuerung
            if command == 0x01:  # Play/Pause
                keyboard.send('play/pause media')
            elif command == 0x02:  # Next
                keyboard.send('next track')
            elif command == 0x03:  # Previous
                keyboard.send('previous track')
            elif command == 0x04:  # Volume Up
                keyboard.send('volume up')
            elif command == 0x05:  # Volume Down
                keyboard.send('volume down')
                
            logging.info(f"Befehl ausgeführt: {hex(command)}")
            
        except Exception as e:
            logging.error(f"Fehler bei Befehlsverarbeitung: {e}")

    def run(self):
        print("Drücken Sie Strg+C zum Beenden")
        
        try:
            while True:
                data = self.device.read(64)
                if data:
                    self.handle_command(data)
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\nProgramm wird beendet...")
        finally:
            self.device.close()

if __name__ == "__main__":
    receiver = SoundboardReceiver()
    receiver.run() 