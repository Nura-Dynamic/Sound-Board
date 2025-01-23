from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import logging
from pathlib import Path
from .audio_effects import AudioEffects
import soundfile as sf

class AudioPlayer:
    def __init__(self, audio_settings):
        """
        Initialisiert den Audio-Player mit den gegebenen Einstellungen
        """
        try:
            self.volume = audio_settings.get('volume', 1.0)
            self.sounds_dir = Path('sounds')
            self.sounds_dir.mkdir(exist_ok=True)
            
            # Media Player für jeden Kanal
            self.players = [QMediaPlayer() for _ in range(16)]
            for player in self.players:
                player.setVolume(int(self.volume * 100))
            
            self.current_player = 0
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
        """
        try:
            sound_path = self.sounds_dir / sound_file
            
            if not sound_path.exists():
                logging.error(f"Audiodatei nicht gefunden: {sound_path}")
                return
                
            # Lade und verarbeite Audio
            audio_data, sample_rate = sf.read(str(sound_path))
            processed = self.effects.process_audio(audio_data, sample_rate)
            
            # Speichere verarbeitetes Audio temporär
            temp_path = self.sounds_dir / f"temp_{sound_file}"
            sf.write(temp_path, processed, sample_rate)
            
            # Wähle nächsten verfügbaren Player
            player = self.players[self.current_player]
            self.current_player = (self.current_player + 1) % len(self.players)
            
            # Spiele Sound ab
            player.setMedia(QMediaContent(QUrl.fromLocalFile(str(temp_path))))
            player.play()
            
        except Exception as e:
            logging.error(f"Fehler beim Abspielen von {sound_file}: {e}")

    def set_volume(self, volume):
        """
        Setzt die Lautstärke (0.0 bis 1.0)
        """
        try:
            self.volume = max(0.0, min(1.0, volume))
            volume_int = int(self.volume * 100)
            for player in self.players:
                player.setVolume(volume_int)
        except Exception as e:
            logging.error(f"Fehler beim Setzen der Lautstärke: {e}")

    def set_channel_volume(self, channel, volume):
        """
        Setzt die Lautstärke für einen bestimmten Kanal
        """
        try:
            if 0 <= channel < len(self.players):
                volume_int = max(0, min(100, int(volume)))
                self.players[channel].setVolume(volume_int)
        except Exception as e:
            logging.error(f"Fehler beim Setzen der Kanal-Lautstärke: {e}") 