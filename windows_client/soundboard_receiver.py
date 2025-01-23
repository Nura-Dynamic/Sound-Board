import hid
import keyboard
import logging
from pathlib import Path
import json
import time
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                            QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import base64

# Icon als Base64-String (ein einfaches Lautsprecher-Icon)
ICON_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAJhSURBVFiF7ZdNaBNBFMd/s9uktqixSG0CUqwgFT+gBw8q6EXwJB4EQcSDINqLX3gQBC2CJ8GT9KB48CKIiCAIgop48CsVRKUgiBUpiFW0tcakJN3ZedhNdrJJNtlNc+nA/GBg583M+8/8Z96bXaWUYjOhN1McqDtYoYBG0TvQKHoHGkVPowKUUhv+6QC2bbewLMuybQchJFJKpJQoJRFCALDaMYQQKKUQQiCEwPO8TGzbxnEcXNfF8zzyPI98Po/neQghSgKEEAghEEIQRREARVFEFEWEYUgYhoRhSBAEBEFAv99n0O8TxzFxHJMkCUmSkCQJruvi+z6DwYB8Pk+hUKBQKGBZVkuSJFiWhed5eJ6H67q4rovv+/i+TxAEhGFIFEXEcUwcxyRJQpqmpGlKmqYopYjjmDiOGQwGDAYDkiQhSRKSJEEpRZqmKKVQSqGUIo5jlFKlWCmFUoooilBKEUURURSVYsMwsCwL0zQxTRPDMLAsC9M0MQwDXdfRNA1d19E0DU3T0DQNXdfRdR1N09A0DV3XMQwDwzAwDANd10t9TdMwDAPTNLEsC8uycBwHx3FwXRfXdXEcB9u2sW0bx3GwbRvLsrAsC8dxcF0Xx3FwHAfP8/A8D9/38X2fIAgIw5AoioiiiDiOieOYJElIkoQkSUiShDRNSdOUNE2J45g4jkmShCRJSJKENE1RSpGmKUopkiQhSRKSJCFJEtI0RSmFUoo0TUnTlCiKiKKIMAwJw5AwDAmCgCAICAKv9CYMgoBCoUChUCCfz5PP5/E8D9d1cRwHx3GwLAvLsnAcB8dxsG0b27axLAvLsv4BQhHjN3hzJHMAAAAASUVORK5CYII=
"""

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
        self.create_tray_icon()
        self.start_hid_thread()
        
        # Zeige Willkommensnachricht im Tray
        self.tray_icon.showMessage(
            "Soundboard Receiver",
            "Läuft im Hintergrund. Klicken Sie hier für mehr Optionen.",
            QSystemTrayIcon.Information,
            3000
        )

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

    def create_tray_icon(self):
        # Erstelle Icon aus Base64-String
        icon_data = base64.b64decode(ICON_BASE64)
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        icon = QIcon(pixmap)
        
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip('Soundboard Receiver')
        
        # Erstelle Kontextmenü
        menu = QMenu()
        
        # Status-Aktion (nicht klickbar)
        self.status_action = menu.addAction("Status: Verbunden")
        self.status_action.setEnabled(False)
        menu.addSeparator()
        
        # Normale Aktionen
        show_action = menu.addAction("Fenster anzeigen")
        show_action.triggered.connect(self.show)
        
        menu.addSeparator()
        quit_action = menu.addAction("Beenden")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()

    def start_hid_thread(self):
        try:
            self.hid_thread = HIDThread(self.VENDOR_ID, self.PRODUCT_ID)
            self.hid_thread.command_received.connect(self.handle_command)
            self.hid_thread.start()
            
            self.status_label.setText("Verbunden und aktiv")
            self.status_action.setText("Status: Verbunden")
            self.tray_icon.setToolTip('Soundboard Receiver (Aktiv)')
            logging.info("HID Thread gestartet")
            
        except Exception as e:
            error_msg = f"Verbindungsfehler: {e}"
            self.status_label.setText("Fehler: Keine Verbindung")
            self.status_action.setText("Status: Nicht verbunden")
            self.tray_icon.setToolTip('Soundboard Receiver (Nicht verbunden)')
            logging.error(error_msg)
            
            # Zeige Fehlermeldung im Tray
            self.tray_icon.showMessage(
                "Verbindungsfehler",
                "Konnte keine Verbindung zum Soundboard herstellen.\n"
                "Bitte überprüfen Sie die USB-Verbindung.",
                QSystemTrayIcon.Warning,
                5000
            )

    def handle_command(self, data):
        try:
            command = data[0]
            command_name = "Unbekannt"
            
            # Mediensteuerung
            if command == 0x01:
                keyboard.send('play/pause media')
                command_name = "Play/Pause"
            elif command == 0x02:
                keyboard.send('next track')
                command_name = "Nächster Track"
            elif command == 0x03:
                keyboard.send('previous track')
                command_name = "Vorheriger Track"
            elif command == 0x04:
                keyboard.send('volume up')
                command_name = "Lauter"
            elif command == 0x05:
                keyboard.send('volume down')
                command_name = "Leiser"
                
            # Aktualisiere Status
            self.status_label.setText(f"Letzter Befehl: {command_name}")
            logging.info(f"Befehl ausgeführt: {command_name} ({hex(command)})")
            
        except Exception as e:
            error_msg = f"Fehler bei Befehlsverarbeitung: {e}"
            self.status_label.setText("Fehler bei Befehlsverarbeitung")
            logging.error(error_msg)
            
            self.tray_icon.showMessage(
                "Fehler",
                "Fehler bei der Befehlsverarbeitung.\n"
                "Siehe Log für Details.",
                QSystemTrayIcon.Warning,
                3000
            )

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