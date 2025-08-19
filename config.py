from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout, 
                            QScrollBar, QLabel, QMainWindow, QPushButton, 
                            QHBoxLayout)
from PyQt5.QtCore import QTimer, QDateTime, Qt, QProcess
import subprocess
import platform
import os 

from PyQt5.QtGui import (
    QTextCursor, QColor, QTextCharFormat, 
    QFont, QFontDatabase
)

BOT_TOKEN = os.getenv('Token')
ID_CHAT = os.getenv('ALLOWED_CHAT_ID')



TRY_NOT_POWERFUL_USER_COMMAND = ['pwd', 'ls', 'time', 'exit', 'quit', 'cd', 
                                'clear', '!help', 'help', 'tgstart', 'tgstop', 
                                'restart', 'rp', 'plugin', 'welcome', 'ns', 'ps', 'joke',
                                'weather', 'powerful']


ALL_COLORS = {
            'text': QColor('#00FF00'),
            'title': QColor("#068B9A"),
            'highlight': QColor('#34E2E2'),
            'normal': QColor("#54EBFF"),
            'time': QColor('#34E2E2'),
            'bg': QColor(30, 30, 30, 230), 
            'network': QColor('#34E2E2'),
            'input': QColor("#FFFFFFFF"),
            'prompt': QColor("#068B9A"),
            'error': QColor("#D90000"),
            'warning': QColor("#EAFF00")
        }


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
        
        
        
class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1000, 415)
        
        
        self.colors = {
            'bg': QColor(30, 30, 30, 230),  
            'text': QColor("#54EBFF"),
            'highlight': QColor('#34E2E2'),  
        }
        
        
        self.setStyleSheet(f"""
            background-color: rgba{self.colors['bg'].getRgb()};
            border-radius: 8px;
            border: 1px solid {self.colors['highlight'].name()};
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        font_id = QFontDatabase.addApplicationFont("VT323-Regular.ttf")  
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text'].name()};
                font-family: {font_family};
                font-size: 60px;
                
            }}
        """)
        self.layout.addWidget(self.label)
        
       
        self.username = os.getenv('USERNAME') or os.getenv('USER') or 'user'
        self.text_to_type = f"|welcome mr.{self.username}| "
        self.current_text = ""
        self.char_index = 0
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_next_char)
        self.timer.start(250) 
        
    def type_next_char(self):
        if self.char_index < len(self.text_to_type):
            self.current_text += self.text_to_type[self.char_index]
            self.label.setText(self.current_text)
            self.char_index += 1
        else:
            self.timer.stop()
            
            QTimer.singleShot(1200, self.close_splash)
            
    def close_splash(self):
        
        self.steps = 30
        self.current_step = 0
        self.start_width = self.width()
        self.start_height = self.height()
        self.start_x = self.x()
        self.start_y = self.y()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_collapse)
        self.timer.start(16) 

    def animate_collapse(self):
       
        self.current_step += 1
        progress = self.current_step / self.steps
        
        new_width = int(self.start_width * (1 - progress))
        new_height = self.start_height 
        
       
        new_x = self.start_x + (self.start_width - new_width) // 2               
        new_y = self.start_y 
        
        
        self.setGeometry(new_x, new_y, new_width, new_height)        
      
        self.setWindowOpacity(1.0 - progress)
               
        if self.current_step >= self.steps:
            self.timer.stop()
            self.close() 
            if self.parent:
                self.parent.show() 