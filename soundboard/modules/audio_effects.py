import pygame
import numpy as np
from scipy import signal
import soundfile as sf
import librosa
import logging

class AudioEffects:
    def __init__(self):
        self.effects = {
            'autotune': {'amount': 50},
            'echo': {'time': 50},
            'reverb': {'size': 50},
            'distortion': {'amount': 50}
        }
        
    def set_effect_param(self, effect_name, param_value):
        """Setzt Parameter für einen Effekt"""
        if effect_name in self.effects:
            param_key = list(self.effects[effect_name].keys())[0]
            self.effects[effect_name][param_key] = param_value
            logging.info(f"Effect {effect_name} {param_key} set to {param_value}")

    def process_audio(self, audio_data, sample_rate):
        """Verarbeitet Audio mit allen aktiven Effekten"""
        processed = audio_data.copy()
        
        # Autotune
        if self.effects['autotune']['amount'] > 0:
            processed = self._apply_autotune(processed, sample_rate)
        
        # Echo
        if self.effects['echo']['time'] > 0:
            processed = self._apply_echo(processed, sample_rate)
            
        # Reverb
        if self.effects['reverb']['size'] > 0:
            processed = self._apply_reverb(processed, sample_rate)
            
        # Distortion
        if self.effects['distortion']['amount'] > 0:
            processed = self._apply_distortion(processed)
            
        return processed

    def _apply_autotune(self, audio_data, sample_rate):
        """Wendet Autotune-Effekt an"""
        try:
            amount = self.effects['autotune']['amount'] / 100.0
            
            # Pitch detection und correction mit librosa
            f0, voiced_flag, _ = librosa.pyin(audio_data, 
                                            fmin=librosa.note_to_hz('C2'),
                                            fmax=librosa.note_to_hz('C7'))
            
            # Nur korrigieren wenn Stimme erkannt wurde
            if voiced_flag.any():
                target_notes = librosa.hz_to_midi(f0[voiced_flag])
                target_notes = np.round(target_notes)
                corrected = librosa.midi_to_hz(target_notes)
                
                # Interpoliere zwischen Original und korrigiertem Pitch
                audio_data[voiced_flag] = librosa.effects.pitch_shift(
                    audio_data[voiced_flag],
                    sr=sample_rate,
                    n_steps=amount * (corrected - f0[voiced_flag])
                )
            
            return audio_data
        except Exception as e:
            logging.error(f"Autotune error: {e}")
            return audio_data

    def _apply_echo(self, audio_data, sample_rate):
        """Wendet Echo-Effekt an"""
        try:
            delay_time = self.effects['echo']['time'] / 100.0  # 0-1 Sekunden
            delay_samples = int(delay_time * sample_rate)
            
            echo = np.zeros_like(audio_data)
            echo[delay_samples:] = audio_data[:-delay_samples] * 0.6
            
            return audio_data + echo
        except Exception as e:
            logging.error(f"Echo error: {e}")
            return audio_data

    def _apply_reverb(self, audio_data, sample_rate):
        """Wendet Reverb-Effekt an"""
        try:
            size = self.effects['reverb']['size'] / 100.0
            
            # Erstelle Impulsantwort für Reverb
            reverb_time = size * 3.0  # Maximale Reverb-Zeit: 3 Sekunden
            impulse_response = np.exp(-np.linspace(0, reverb_time, int(reverb_time * sample_rate)))
            
            # Konvolution für Reverb-Effekt
            reverb = signal.convolve(audio_data, impulse_response, mode='full')[:len(audio_data)]
            
            return audio_data * (1 - size) + reverb * size
        except Exception as e:
            logging.error(f"Reverb error: {e}")
            return audio_data

    def _apply_distortion(self, audio_data):
        """Wendet Distortion-Effekt an"""
        try:
            amount = self.effects['distortion']['amount'] / 100.0
            
            # Soft clipping Distortion
            threshold = 1.0 - (amount * 0.9)
            processed = np.clip(audio_data, -threshold, threshold)
            processed = np.tanh(processed * (1 + amount * 10)) * 0.9
            
            return processed
        except Exception as e:
            logging.error(f"Distortion error: {e}")
            return audio_data 