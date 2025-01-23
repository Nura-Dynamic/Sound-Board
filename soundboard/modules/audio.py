import pygame
import logging
from pathlib import Path
from .audio_effects import AudioEffects
import numpy as np
import soundfile as sf

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
            
            self.sound_cache = {}
            self.effects = AudioEffects()
            
            logging.info("Audio-Player erfolgreich initialisiert")
            
        except Exception as e:
            logging.error(f"Fehler bei Audio-Player-Initialisierung: {e}")
            raise

    def set_effect_param(self, effect_name, value):
        """Setzt Parameter für einen Audio-Effekt"""
        self.effects.set_effect_param(effect_name, value)

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
                
            # Lade Audio mit soundfile
            audio_data, sample_rate = sf.read(str(sound_path))
            
            # Wende Effekte an
            processed = self.effects.process_audio(audio_data, sample_rate)
            
            # Speichere verarbeitetes Audio temporär
            temp_path = self.sounds_dir / f"temp_{sound_file}"
            sf.write(temp_path, processed, sample_rate)
            
            # Lade Sound aus Cache oder neu
            self.sound_cache[str(sound_path)] = pygame.mixer.Sound(str(temp_path))
            
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