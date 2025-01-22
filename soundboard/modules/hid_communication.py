import usb.core
import usb.util
import logging
from time import sleep

class HIDCommunication:
    # Standard HID Keyboard Modifiers
    MODIFIER_NONE  = 0x00
    MODIFIER_CTRL  = 0x01
    MODIFIER_SHIFT = 0x02
    MODIFIER_ALT   = 0x04
    
    def __init__(self, vendor_id=0x0483, product_id=0x5750):
        """
        Initialisiert die USB HID-Kommunikation
        
        :param vendor_id: USB Vendor ID
        :param product_id: USB Product ID
        """
        try:
            # Finde das USB-Gerät
            self.device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
            
            if self.device is None:
                logging.info("HID-Gerät nicht gefunden - Offline-Modus aktiv")
                self.emulation_mode = True
            else:
                self.emulation_mode = False
                # Setze USB-Konfiguration
                try:
                    self.device.set_configuration()
                    logging.info("HID-Gerät erfolgreich verbunden")
                except usb.core.USBError as e:
                    logging.warning(f"Konnte HID-Gerät nicht konfigurieren: {e}")
                    self.emulation_mode = True
            
        except Exception as e:
            logging.info(f"HID-Kommunikation nicht verfügbar: {e}")
            self.emulation_mode = True

    def send_command(self, command):
        """
        Sendet einen Befehl als HID-Tastenkombination
        
        :param command: String mit dem Befehl (z.B. "play_pause")
        """
        try:
            if self.emulation_mode:
                logging.debug(f"Offline-Modus: HID-Befehl {command} ignoriert")
                return
                
            # Mapping von Befehlen zu HID-Codes
            command_mapping = {
                "play_pause": ([self.MODIFIER_NONE], [0x2C]),  # Leertaste
                "volume_up": ([self.MODIFIER_NONE], [0x80]),   # Volume Up
                "volume_down": ([self.MODIFIER_NONE], [0x81])  # Volume Down
            }
            
            if command in command_mapping:
                modifiers, keycodes = command_mapping[command]
                self._send_keyboard_report(modifiers, keycodes)
                # Kurze Verzögerung und Reset
                sleep(0.05)
                self._send_keyboard_report([self.MODIFIER_NONE], [0x00])
            else:
                logging.warning(f"Unbekannter Befehl: {command}")
                
        except Exception as e:
            logging.warning(f"HID-Befehl konnte nicht gesendet werden: {e}")
            self.emulation_mode = True  # Schalte in Offline-Modus bei Fehlern

    def _send_keyboard_report(self, modifiers, keycodes):
        """
        Sendet einen USB HID Keyboard Report
        
        :param modifiers: Liste der Modifier-Bytes
        :param keycodes: Liste der Keycode-Bytes
        """
        try:
            # Standard HID Keyboard Report
            report = [0] * 8
            report[0] = modifiers[0]  # Modifier byte
            report[2:8] = keycodes + [0] * (6 - len(keycodes))  # Key array
            
            # Sende Report
            self.device.ctrl_transfer(
                0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
                0x09,  # SET_REPORT
                0x200, # Report Type + Report ID
                0,     # Interface
                report # Report Data
            )
            
        except Exception as e:
            logging.error(f"Fehler beim Senden des Keyboard Reports: {e}") 