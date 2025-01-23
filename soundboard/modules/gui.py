from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QGridLayout, 
                            QVBoxLayout, QHBoxLayout, QSlider, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
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
        main_layout.setSpacing(5)  # Geringerer Abstand für 10 Zoll
        main_layout.setContentsMargins(5, 5, 5, 5)  # Kleinere Ränder
        
        # Linke Seite: Soundboard-Buttons (70% der Breite)
        left_widget = QWidget()
        grid = QGridLayout(left_widget)
        grid.setSpacing(5)  # Geringerer Abstand zwischen Buttons
        
        # Vordefinierte Button-Konfiguration
        button_configs = {
            '0': {'text': 'Sound 1', 'type': 'sound'},
            '1': {'text': 'Sound 2', 'type': 'sound'},
            '2': {'text': 'Play', 'type': 'play'},
            '3': {'text': 'Stop', 'type': 'stop'},
            '4': {'text': 'Auto', 'type': 'autotune'},  # Kürzere Namen
            '5': {'text': 'Echo', 'type': 'effect'},
            '6': {'text': 'Rev', 'type': 'effect'},     # Kürzere Namen
            '7': {'text': 'Dist', 'type': 'effect'}     # Kürzere Namen
        }
        
        # Erstelle Buttons
        button_font = QFont()
        button_font.setPointSize(14)  # Größere Schrift für Touch
        
        for row in range(4):
            for col in range(4):
                button_id = str(row * 4 + col)
                config = button_configs.get(button_id, {
                    'text': f'B{int(button_id) + 1}',  # Kürzere Namen
                    'type': 'default'
                })
                
                button = QPushButton(config['text'])
                button.setFont(button_font)
                button.setMinimumSize(120, 80)  # Angepasste Größe für 10 Zoll
                
                color = self.button_colors[config['type']]
                style = f"""
                    QPushButton {{
                        background-color: {color.name()};
                        border: 2px solid #666666;
                        border-radius: 8px;
                        font-weight: bold;
                    }}
                    QPushButton:pressed {{
                        background-color: #666666;
                        border-style: inset;
                    }}
                """
                button.setStyleSheet(style)
                button.clicked.connect(lambda checked, x=button_id: self.button_callback(x))
                grid.addWidget(button, row, col)
        
        # Rechte Seite: Mixer und Effekte (30% der Breite)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(5)
        
        # Lautstärkeregler
        mixer_widget = QWidget()
        mixer_layout = QHBoxLayout(mixer_widget)
        mixer_layout.setSpacing(2)  # Sehr geringer Abstand
        
        # Erstelle 4 Lautstärkeregler
        for i in range(4):
            slider_container = QWidget()
            slider_layout = QVBoxLayout(slider_container)
            slider_layout.setSpacing(2)
            
            # Label
            label = QLabel(f"Ch {i+1}")  # Kürzere Namen
            label.setFont(button_font)
            label.setStyleSheet("color: white;")
            label.setAlignment(Qt.AlignCenter)
            
            # Slider
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(75)
            slider.setMinimumHeight(150)  # Angepasste Höhe
            slider.setStyleSheet("""
                QSlider::groove:vertical {
                    background: #666666;
                    width: 12px;
                    border-radius: 6px;
                }
                QSlider::handle:vertical {
                    background: #00ff00;
                    height: 20px;
                    width: 20px;
                    margin: -2px -4px;
                    border-radius: 10px;
                }
            """)
            
            # Level-Anzeige
            level = QLabel("75")  # Kürzerer Text
            level.setFont(button_font)
            level.setStyleSheet("color: white;")
            level.setAlignment(Qt.AlignCenter)
            
            slider.valueChanged.connect(lambda v, l=level: l.setText(str(v)))
            
            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(level)
            mixer_layout.addWidget(slider_container)
        
        right_layout.addWidget(mixer_widget)
        
        # Effekt-Parameter
        effects_widget = QWidget()
        effects_layout = QGridLayout(effects_widget)
        effects_layout.setSpacing(5)
        
        effect_params = [
            "Auto", "Echo", "Rev", "Dist"  # Kürzere Namen
        ]
        
        for i, param in enumerate(effect_params):
            label = QLabel(param)
            label.setFont(button_font)
            label.setStyleSheet("color: white;")
            
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    background: #666666;
                    height: 12px;
                    border-radius: 6px;
                }
                QSlider::handle:horizontal {
                    background: #ff00ff;
                    width: 20px;
                    margin: -4px 0;
                    border-radius: 10px;
                }
            """)
            
            effects_layout.addWidget(label, i, 0)
            effects_layout.addWidget(slider, i, 1)
        
        right_layout.addWidget(effects_widget)
        
        # Layout-Verhältnis anpassen
        main_layout.addWidget(left_widget, stretch=7)  # 70%
        main_layout.addWidget(right_widget, stretch=3) # 30%
        
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