import pygame
import logging
import os

# X11-Display wird automatisch erkannt

class SoundboardGUI:
    def __init__(self, button_callback, config):
        """Initialisiert die Pygame-basierte GUI"""
        try:
            pygame.init()
            # Initialisiere nur das Display-Modul
            pygame.display.init()
            pygame.font.init()
            
            self.config = config
            # Bildschirmgröße ermitteln
            info = pygame.display.Info()
            # Verwende volle Bildschirmgröße für Touchscreen
            self.width = info.current_w
            self.height = info.current_h
            
            # Vollbild-Modus für Touchscreen
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.NOFRAME)
            pygame.display.set_caption('Soundboard')
            pygame.mouse.set_visible(False)  # Verstecke Maus-Cursor für Touch
            
            # Touch-Optimierungen
            pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])
            
            # Farben aus Konfiguration laden
            self.background_color = tuple(self.config['gui_settings']['background_color'])
            self.feedback_color = tuple(self.config['gui_settings']['feedback_color'])
            
            # Button-Grid erstellen
            self.buttons = self._create_buttons()
            self.callback = button_callback
            
            logging.info("GUI erfolgreich initialisiert")
            
        except Exception as e:
            logging.error(f"Fehler bei GUI-Initialisierung: {e}")
            raise

    def _create_buttons(self):
        """Erstellt das 4x4 Button-Grid"""
        buttons = []
        margin = self.config['gui_settings']['button_margin']
        cols, rows = 4, 4
        
        # Buttongrößen berechnen
        button_width = (self.width - (cols + 1) * margin) // cols
        button_height = (self.height - (rows + 1) * margin) // rows
        
        for row in range(rows):
            for col in range(cols):
                x = margin + col * (button_width + margin)
                y = margin + row * (button_height + margin)
                button_id = str(row * cols + col)
                
                # Button-Konfiguration aus config laden
                button_config = self.config['buttons'].get(button_id, {
                    "text": f"Button {button_id}",
                    "color": [255, 255, 255]
                })
                
                button = {
                    'rect': pygame.Rect(x, y, button_width, button_height),
                    'id': button_id,
                    'text': button_config['text'],
                    'pressed': False,
                    'color': tuple(button_config['color']),
                    'original_color': tuple(button_config['color'])
                }
                buttons.append(button)
                
        return buttons

    def run(self):
        """Hauptschleife der GUI"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Numpad für direkte Button-Auswahl
                    elif event.key in range(pygame.K_KP0, pygame.K_KP9 + 1):
                        button_id = str(event.key - pygame.K_KP0)
                        self._trigger_button(button_id)
            
            self._draw()
            clock.tick(60)  # Höhere Framerate für bessere Reaktionszeit
            
        pygame.quit()

    def _handle_click(self, pos):
        """Verarbeitet Mausklicks/Touchscreen-Events"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                button['pressed'] = True
                button['color'] = self.feedback_color
                self.callback(button['id'])
                # Visual feedback
                self._draw()
                pygame.time.wait(100)
                button['pressed'] = False
                button['color'] = button['original_color']
                break

    def _draw(self):
        """Zeichnet die Benutzeroberfläche"""
        self.screen.fill(self.background_color)
        
        for button in self.buttons:
            color = self.feedback_color if button['pressed'] else button['color']
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, self.background_color, button['rect'], 2)  # Rahmen
            
            # Text rendern
            font = pygame.font.Font(None, self.config['gui_settings']['font_size'])
            text = font.render(button['text'], True, self.background_color)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def _trigger_button(self, button_id):
        """Löst einen Button programmatisch aus"""
        for button in self.buttons:
            if button['id'] == button_id:
                button['pressed'] = True
                button['color'] = self.feedback_color
                self.callback(button['id'])
                self._draw()
                pygame.time.wait(100)
                button['pressed'] = False
                button['color'] = button['original_color']
                break 