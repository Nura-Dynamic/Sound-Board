import pygame
import logging
from pathlib import Path

class AudioPlayer:
    def __init__(self, audio_settings):
        """
        Initialisiert den Audio-Player mit den gegebenen Einstellungen
        
        :param audio_settings: Dict mit Audio-Einstellungen (output_device, volume)
        """
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(16)  # Erlaubt mehrere gleichzeitige Sounds
            
            self.volume = audio_settings.get('volume', 1.0)
            pygame.mixer.music.set_volume(self.volume)
            
            self.sounds_dir = Path('sounds')
            self.sounds_dir.mkdir(exist_ok=True)
            
            self.sound_cache = {}  # Cache für geladene Sounds
            logging.info("Audio-Player erfolgreich initialisiert")
            
        except Exception as e:
            logging.error(f"Fehler bei Audio-Player-Initialisierung: {e}")
            raise

    def play(self, sound_file):
        """
        Spielt eine Audiodatei ab
        
        :param sound_file: Name der Audiodatei
        """
        try:
            sound_path = self.sounds_dir / sound_file
            
            if not sound_path.exists():
                logging.error(f"Audiodatei nicht gefunden: {sound_path}")
                return
                
            # Lade Sound aus Cache oder neu
            if str(sound_path) not in self.sound_cache:
                self.sound_cache[str(sound_path)] = pygame.mixer.Sound(str(sound_path))
            
            self.sound_cache[str(sound_path)].play()
            
        except Exception as e:
            logging.error(f"Fehler beim Abspielen von {sound_file}: {e}")

    def set_volume(self, volume):
        """
        Setzt die Lautstärke (0.0 bis 1.0)
        """
        try:
            self.volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(self.volume)
        except Exception as e:
            logging.error(f"Fehler beim Setzen der Lautstärke: {e}") 