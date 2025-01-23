import usb.core
import usb.util
import logging

class HIDDevice:
    def __init__(self):
        self.VENDOR_ID = 0x0483  # Standard ST-Microelectronics ID
        self.PRODUCT_ID = 0x5750 # Beliebige ID für unser Gerät
        self.device = None
        self.ep = None
        self.setup_device()

    def setup_device(self):
        try:
            # Finde das USB-Gerät
            self.device = usb.core.find(idVendor=self.VENDOR_ID)
            
            if self.device is None:
                # Wenn nicht gefunden, erstelle ein neues HID-Gerät
                self.create_hid_device()
            
            # Setze USB-Konfiguration
            self.device.set_configuration()
            
            # Finde den HID-Endpunkt
            cfg = self.device.get_active_configuration()
            intf = cfg[(0,0)]
            
            self.ep = usb.util.find_descriptor(
                intf,
                custom_match = lambda e: 
                    usb.util.endpoint_direction(e.bEndpointAddress) == 
                    usb.util.ENDPOINT_OUT
            )
            
            logging.info("HID-Gerät erfolgreich initialisiert")
            
        except Exception as e:
            logging.error(f"Fehler bei HID-Initialisierung: {e}")
            raise

    def send_command(self, command):
        """Sendet einen HID-Befehl"""
        try:
            if self.ep:
                self.ep.write([command])
                logging.info(f"HID-Befehl gesendet: {hex(command)}")
        except Exception as e:
            logging.error(f"Fehler beim Senden des HID-Befehls: {e}") 