from gpiozero import Button
import logging

class GPIOHandler:
    def __init__(self, gpio_pins, callback):
        """
        Initialisiert die GPIO-Pins für Tasteneingang
        
        :param gpio_pins: Liste der GPIO-Pin-Nummern
        :param callback: Funktion die bei Tastendruck aufgerufen wird
        """
        self.buttons = {}
        try:
            for pin in gpio_pins:
                # Pull-up Widerstand aktiviert, Button ist active-low
                button = Button(pin, pull_up=True, bounce_time=0.05)
                button.when_pressed = lambda p=pin: callback(p)
                self.buttons[pin] = button
                
            logging.info(f"GPIO-Handler initialisiert für Pins: {gpio_pins}")
            
        except Exception as e:
            logging.error(f"Fehler bei GPIO-Initialisierung: {e}")
            raise

    def cleanup(self):
        """
        Gibt die GPIO-Ressourcen frei
        """
        try:
            for button in self.buttons.values():
                button.close()
            logging.info("GPIO-Ressourcen freigegeben")
        except Exception as e:
            logging.error(f"Fehler beim GPIO-Cleanup: {e}") 