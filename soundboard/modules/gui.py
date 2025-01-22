import pygame
import logging
import os
os.environ['SDL_VIDEODRIVER'] = 'fbcon'  # Für direkten Framebuffer-Zugriff

class SoundboardGUI:
    def __init__(self, button_callback):
        """Initialisiert die Pygame-basierte GUI"""
        try:
            pygame.init()
            pygame.display.init()
            
            # Bildschirmgröße ermitteln
            info = pygame.display.Info()
            self.width = info.current_w
            self.height = info.current_h
            
            # Vollbild-Modus
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Soundboard')
            
            # Farben definieren
            self.BLACK = (0, 0, 0)
            self.WHITE = (255, 255, 255)
            self.GRAY = (128, 128, 128)
            
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
        margin = 10
        cols, rows = 4, 4
        
        # Buttongrößen berechnen
        button_width = (self.width - (cols + 1) * margin) // cols
        button_height = (self.height - (rows + 1) * margin) // rows
        
        for row in range(rows):
            for col in range(cols):
                x = margin + col * (button_width + margin)
                y = margin + row * (button_height + margin)
                button_id = row * cols + col
                
                button = {
                    'rect': pygame.Rect(x, y, button_width, button_height),
                    'id': button_id,
                    'text': f'Button {button_id}',
                    'pressed': False
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
            
            self._draw()
            clock.tick(30)
            
        pygame.quit()

    def _handle_click(self, pos):
        """Verarbeitet Mausklicks/Touchscreen-Events"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                button['pressed'] = True
                self.callback(button['id'])
                # Visual feedback
                self._draw()
                pygame.time.wait(100)
                button['pressed'] = False
                break

    def _draw(self):
        """Zeichnet die Benutzeroberfläche"""
        self.screen.fill(self.BLACK)
        
        for button in self.buttons:
            color = self.GRAY if button['pressed'] else self.WHITE
            pygame.draw.rect(self.screen, color, button['rect'])
            
            # Text rendern
            font = pygame.font.Font(None, 36)
            text = font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip() 