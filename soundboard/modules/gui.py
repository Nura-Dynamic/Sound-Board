from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt
import sys
import logging

class SoundboardGUI(QMainWindow):
    def __init__(self, button_callback):
        # Stelle sicher, dass QApplication existiert
        if not QApplication.instance():
            raise RuntimeError("QApplication muss vor SoundboardGUI erstellt werden")
        
        super().__init__()
        self.button_callback = button_callback
        self.init_ui()

    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        self.setWindowTitle('Soundboard')
        self.setGeometry(0, 0, 800, 480)  # Für 10-Zoll Display
        
        # Erstelle zentrales Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid = QGridLayout(central_widget)
        
        # Erstelle 4x4 Grid mit Buttons
        for row in range(4):
            for col in range(4):
                button_id = row * 4 + col
                button = QPushButton(f'Button {button_id}')
                button.setMinimumSize(180, 100)
                button.clicked.connect(lambda checked, x=button_id: self.button_callback(x))
                grid.addWidget(button, row, col)

    def show(self):
        """Überschreibt die show()-Methode"""
        # Vollbildmodus aktivieren
        self.showFullScreen() 