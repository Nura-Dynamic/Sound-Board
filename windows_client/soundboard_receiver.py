import hid
import keyboard
import logging
from pathlib import Path
import json
import time
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                            QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class HIDThread(QThread):
    command_received = pyqtSignal(list)
    
    def __init__(self, vendor_id, product_id):
        super().__init__()
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.running = True
        
    def run(self):
        try:
            device = hid.device()
            device.open(self.vendor_id, self.product_id)
            device.set_nonblocking(True)
            
            while self.running:
                data = device.read(64)
                if data:
                    self.command_received.emit(data)
                time.sleep(0.01)
                
        except Exception as e:
            logging.error(f"HID Thread Error: {e}")
        finally:
            try:
                device.close()
            except:
                pass

class SoundboardReceiver(QWidget):
    def __init__(self):
        super().__init__()
        self.VENDOR_ID = 0x0483
        self.PRODUCT_ID = 0x5750
        
        self.setup_logging()
        self.load_config()
        self.init_ui()
        self.init_tray()
        self.start_hid_thread()
        
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

    def init_ui(self):
        self.setWindowTitle('Soundboard Receiver')
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Status Label
        self.status_label = QLabel("Warte auf Verbindung...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Minimize Button
        minimize_btn = QPushButton("In Tray minimieren")
        minimize_btn.clicked.connect(self.hide)
        layout.addWidget(minimize_btn)
        
        self.setLayout(layout)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip('Soundboard Receiver')
        
        # Erstelle ein Kontextmenü
        menu = QMenu()
        show_action = menu.addAction("Anzeigen")
        show_action.triggered.connect(self.show)
        quit_action = menu.addAction("Beenden")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def start_hid_thread(self):
        self.hid_thread = HIDThread(self.VENDOR_ID, self.PRODUCT_ID)
        self.hid_thread.command_received.connect(self.handle_command)
        self.hid_thread.start()
        
        self.status_label.setText("Verbunden und aktiv")
        logging.info("HID Thread gestartet")

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

    def quit_app(self):
        self.hid_thread.running = False
        self.hid_thread.wait()
        QApplication.quit()

    def closeEvent(self, event):
        # Beim Klick auf X nur minimieren statt beenden
        event.ignore()
        self.hide()

def main():
    import sys
    app = QApplication(sys.argv)
    
    # Verhindere, dass die App sich beendet wenn das letzte Fenster geschlossen wird
    app.setQuitOnLastWindowClosed(False)
    
    receiver = SoundboardReceiver()
    receiver.show()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main()) 