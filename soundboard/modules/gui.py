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
            
            # Farben für das neue Design
            self.background_color = (0, 0, 0)  # Schwarzer Hintergrund
            self.button_colors = {
                'default': (255, 255, 255),  # Weiß
                'sound': (200, 200, 255),    # Hellblau
                'play': (200, 255, 200),     # Hellgrün
                'stop': (255, 200, 200)      # Hellrot
            }
            self.feedback_color = (100, 100, 100)  # Dunkelgrau für Feedback
            
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
        margin = 10  # Kleinerer Rand für mehr Platz
        cols, rows = 4, 4
        
        button_width = (self.width - (cols + 1) * margin) // cols
        button_height = (self.height - (rows + 1) * margin) // rows
        
        # Vordefinierte Button-Konfiguration
        button_configs = {
            '0': {'text': 'Sound 1', 'type': 'sound'},
            '1': {'text': 'Sound 2', 'type': 'sound'},
            '2': {'text': 'Play', 'type': 'play'},
            '3': {'text': 'Stop', 'type': 'stop'},
            # Weitere Buttons mit Standardwerten
        }
        
        for row in range(rows):
            for col in range(cols):
                x = margin + col * (button_width + margin)
                y = margin + row * (button_height + margin)
                button_id = str(row * cols + col)
                
                # Button-Konfiguration mit Fallback
                config = button_configs.get(button_id, {
                    'text': f'Button {int(button_id) + 1}',
                    'type': 'default'
                })
                
                button = {
                    'rect': pygame.Rect(x, y, button_width, button_height),
                    'id': button_id,
                    'text': config['text'],
                    'pressed': False,
                    'color': self.button_colors[config['type']],
                    'original_color': self.button_colors[config['type']]
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
            
            # Button mit abgerundeten Ecken
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=10)
            
            # Größerer, deutlicherer Text
            font = pygame.font.Font(None, 36)
            text = font.render(button['text'], True, (0, 0, 0))  # Schwarzer Text
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