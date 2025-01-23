from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QGridLayout, 
                            QVBoxLayout, QHBoxLayout, QSlider, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import logging

class SoundboardGUI(QMainWindow):
    def __init__(self, button_callback, config):
        """Initialisiert die Qt-basierte GUI"""
        super().__init__()
        self.button_callback = button_callback
        self.config = config
        
        # Farben für das Design
        self.button_colors = {
            'default': QColor(255, 255, 255),  # Weiß
            'sound': QColor(200, 200, 255),    # Hellblau
            'play': QColor(200, 255, 200),     # Hellgrün
            'stop': QColor(255, 200, 200),     # Hellrot
            'effect': QColor(255, 200, 255),   # Pink für Effekte
            'autotune': QColor(200, 255, 255)  # Türkis für Autotune
        }
        
        try:
            self.init_ui()
            logging.info("GUI erfolgreich initialisiert")
        except Exception as e:
            logging.error(f"Fehler bei GUI-Initialisierung: {e}")
            raise

    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        self.setWindowTitle('Soundboard')
        self.setWindowFlags(Qt.FramelessWindowHint)  # Keine Fensterrahmen
        self.showFullScreen()
        
        # Hauptlayout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Linke Seite: Soundboard-Buttons
        left_widget = QWidget()
        grid = QGridLayout(left_widget)
        grid.setSpacing(10)
        
        # Vordefinierte Button-Konfiguration
        button_configs = {
            '0': {'text': 'Sound 1', 'type': 'sound'},
            '1': {'text': 'Sound 2', 'type': 'sound'},
            '2': {'text': 'Play', 'type': 'play'},
            '3': {'text': 'Stop', 'type': 'stop'},
            '4': {'text': 'Autotune', 'type': 'autotune'},
            '5': {'text': 'Echo', 'type': 'effect'},
            '6': {'text': 'Reverb', 'type': 'effect'},
            '7': {'text': 'Distortion', 'type': 'effect'}
        }
        
        # Erstelle Buttons
        for row in range(4):
            for col in range(4):
                button_id = str(row * 4 + col)
                config = button_configs.get(button_id, {
                    'text': f'Button {int(button_id) + 1}',
                    'type': 'default'
                })
                
                button = QPushButton(config['text'])
                button.setMinimumSize(180, 100)
                
                color = self.button_colors[config['type']]
                style = f"""
                    QPushButton {{
                        background-color: {color.name()};
                        border: 2px solid #666666;
                        border-radius: 10px;
                        font-size: 24px;
                        font-weight: bold;
                    }}
                    QPushButton:pressed {{
                        background-color: #666666;
                    }}
                """
                button.setStyleSheet(style)
                button.clicked.connect(lambda checked, x=button_id: self.button_callback(x))
                grid.addWidget(button, row, col)
        
        # Rechte Seite: Mixer und Effekte
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Lautstärkeregler
        mixer_widget = QWidget()
        mixer_layout = QHBoxLayout(mixer_widget)
        
        # Erstelle 4 Lautstärkeregler
        for i in range(4):
            slider_container = QWidget()
            slider_layout = QVBoxLayout(slider_container)
            
            # Label
            label = QLabel(f"Channel {i+1}")
            label.setStyleSheet("color: white; font-size: 18px;")
            label.setAlignment(Qt.AlignCenter)
            
            # Slider
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(75)
            slider.setMinimumHeight(200)
            slider.setStyleSheet("""
                QSlider::groove:vertical {
                    background: #666666;
                    width: 20px;
                    border-radius: 10px;
                }
                QSlider::handle:vertical {
                    background: #00ff00;
                    height: 30px;
                    width: 30px;
                    margin: -4px -5px;
                    border-radius: 15px;
                }
            """)
            
            # Level-Anzeige
            level = QLabel("75%")
            level.setStyleSheet("color: white; font-size: 16px;")
            level.setAlignment(Qt.AlignCenter)
            
            slider.valueChanged.connect(lambda v, l=level: l.setText(f"{v}%"))
            
            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(level)
            mixer_layout.addWidget(slider_container)
        
        right_layout.addWidget(mixer_widget)
        
        # Effekt-Parameter
        effects_widget = QWidget()
        effects_layout = QGridLayout(effects_widget)
        
        effect_params = [
            "Autotune Amount", "Echo Time", 
            "Reverb Size", "Distortion"
        ]
        
        for i, param in enumerate(effect_params):
            label = QLabel(param)
            label.setStyleSheet("color: white; font-size: 16px;")
            
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    background: #666666;
                    height: 20px;
                    border-radius: 10px;
                }
                QSlider::handle:horizontal {
                    background: #ff00ff;
                    width: 30px;
                    margin: -5px 0;
                    border-radius: 15px;
                }
            """)
            
            effects_layout.addWidget(label, i, 0)
            effects_layout.addWidget(slider, i, 1)
        
        right_layout.addWidget(effects_widget)
        
        # Füge beide Seiten zum Hauptlayout hinzu
        main_layout.addWidget(left_widget, stretch=2)
        main_layout.addWidget(right_widget, stretch=1)
        
        # Setze schwarzen Hintergrund
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

    def keyPressEvent(self, event):
        """Behandelt Tastatureingaben"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event) 