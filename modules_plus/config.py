from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout, 
                            QScrollBar, QLabel, QMainWindow, QPushButton, 
                            QHBoxLayout)
import subprocess
import platform

TITLE_BAR_STYLE = """
    border: 1px solid #34E2E2;
    border-bottom: none;
    background: #000000;
"""

BUTTON_STYLE = """
    QPushButton {
        background: transparent;
        color: white;
        font-size: 14px;
        border: none;
    }
"""

CLOSE_BUTTON_HOVER = """
    QPushButton:hover {
        background: #E81123;
    }
"""

MINIMIZE_BUTTON_HOVER = """
    QPushButton:hover {
        background: #2D2D2D;
    }
"""

TITLE_STYLE = """
    color: #068B9A;
    font-family: Arial;
    font-size: 16px;
    font-weight: bold;
    padding-left: 2px;
"""

WINDOW_STYLE = """
    QWidget {
        border: 1px solid #34E2E2;
        background: #000000;
    }
"""
THEMES = {
    'dark': {'bg': '#000000', 'text': '#00FF00'},
    'light': {'bg': '#FFFFFF', 'text': '#000000'},
    'matrix': {'bg': '#001F00', 'text': '#00FF41'}
}
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet(TITLE_BAR_STYLE)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet(BUTTON_STYLE + CLOSE_BUTTON_HOVER)
        self.close_btn.clicked.connect(parent.close)
        
        self.minimize_btn = QPushButton("—")
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.setStyleSheet(BUTTON_STYLE + MINIMIZE_BUTTON_HOVER)
        self.minimize_btn.clicked.connect(parent.showMinimized)
        
        self.title = QLabel("ultimatum@arch")
        self.title.setStyleSheet(TITLE_STYLE)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.close_btn)

