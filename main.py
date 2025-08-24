
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from config import CustomTitleBar, SplashScreen, WINDOW_STYLE
from arch_Linux_main import ArchTerminal

import warnings
warnings.filterwarnings("ignore", message="python-telegram-bot is using upstream urllib3")
warnings.filterwarnings("ignore", message="pkg_resources is deprecated") #Временно


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1000, 415)
        self.setStyleSheet("QMainWindow { background: transparent; }")
        
        self.title_bar = CustomTitleBar(self)
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_bar)
        
        self.terminal = ArchTerminal()
        layout.addWidget(self.terminal)
        
        self.setCentralWidget(container)
        
        self.setup_dragging()
        
        if os.getenv("WELCOME_WINDOW", "0") == "1":
            self.show_splash_screen()
    
    def setup_dragging(self):
        def move_window(event):
            if event.buttons() == Qt.LeftButton:
                self.move(event.globalPos() - self.title_bar.drag_pos)
        
        def mouse_press_event(event):
            if event.button() == Qt.LeftButton:
                self.title_bar.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
        
        self.title_bar.mouseMoveEvent = move_window
        self.title_bar.mousePressEvent = mouse_press_event
    
    def show_splash_screen(self):
        splash = SplashScreen(self)
        splash.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())