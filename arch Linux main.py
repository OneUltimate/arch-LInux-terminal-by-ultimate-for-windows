import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout, 
                            QScrollBar, QLabel, QMainWindow, QPushButton, 
                            QHBoxLayout)
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont
import platform
import psutil
import datetime
import time
import subprocess

from weather import *
from cpuinformation import *
from testirovka import *
from cheking_system import *
from proxy_checker import * 

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

class ArchTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(WINDOW_STYLE)
        self.setWindowTitle("ultimatum@arch")
        self.setGeometry(100, 100, 1000, 415)
        
        self.colors = {
            'text': QColor('#00FF00'),
            'title': QColor("#068B9A"),
            'highlight': QColor('#34E2E2'),
            'normal': QColor('#D3D7CF'),
            'time': QColor('#34E2E2'),
            'bg': QColor('#000000'),
            'network': QColor('#34E2E2')
        }
        
        self.font = QFont("Consolas", 10)
        self.last_ip = ""
        self.last_network = ""
        
        self.init_ui()
        self.display_system_info()
        self.setup_timers()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(layout)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(self.font)
        self.terminal.setStyleSheet(f"background-color: {self.colors['bg'].name()};")
        self.terminal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        layout.addWidget(self.terminal)
    
    def add_line(self, text, color=None, auto_scroll=False):
        scrollbar = self.terminal.verticalScrollBar()
        old_scroll_pos = scrollbar.value()
        
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if color:
            format = QTextCharFormat()
            format.setForeground(self.colors[color])
            cursor.setCharFormat(format)
        
        cursor.insertText(text + "\n")
        
        if not auto_scroll:
            scrollbar.setValue(old_scroll_pos)
    
    def update_line(self, prefix, new_value, color=None):
        """Общий метод для обновления строк с префиксом"""
        text = self.terminal.toPlainText()
        pos = text.rfind(prefix)
        
        if pos == -1:
            self.add_line(f"                                      |{prefix}{new_value}", color or 'normal', auto_scroll=False)
        else:
            scrollbar = self.terminal.verticalScrollBar()
            old_scroll_pos = scrollbar.value()
            
            cursor = self.terminal.textCursor()
            cursor.setPosition(pos + len(prefix))
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            
            if color:
                format = QTextCharFormat()
                format.setForeground(self.colors[color])
                cursor.setCharFormat(format)
            
            cursor.insertText(new_value)
            scrollbar.setValue(old_scroll_pos)
    
    def display_system_info(self):
        self.terminal.clear()
        
        os_info = f"                                      |OS: {platform.system()} {platform.release()}"
        kernel = f"                                      |Kernel: {platform.release()}"
        
        uptime = datetime.timedelta(seconds=time.time()-psutil.boot_time())
        uptime_str = str(uptime).split('.')[0]
        
        try:
            packages = subprocess.check_output(["pacman", "-Qq"]).decode().count('\n')
        except:
            packages = "N/A"
        
        shell = psutil.Process().parent().name()
        
        mem = psutil.virtual_memory()
        mem_used = mem.used / (1024**3) 
        mem_total = mem.total / (1024**3) * 2
        
        cpu_info = 'amd ryzen 5 1600 8 CPU 3.20GHZ' if mem_used > 5 else nameCPU
        gpu_info = 'rtx2060' if mem_used > 5 else get_gpu_info()
        
        cpu_temp = cputemp()
        temperature = temp1()
        ip_address = self.get_ip_address()
        cpuresinfo = get_gpu_info_resolution()
        cheksys = check_inf_windows()
        proxy_tf = get_system_proxy()
        
        self.add_line("--------------------------------", 'highlight')
        self.add_line(f'{os_info}', auto_scroll=False)
        self.add_line(f'{kernel}', auto_scroll=False)
       
       
        self.update_line("Time: ", QDateTime.currentDateTime().toString("HH:mm:ss"), 'time')
        
        self.add_line(f"                *                     |Uptime: {uptime_str}", auto_scroll=False)
        self.add_line(f"               ***                    |Host: {platform.node()}", auto_scroll=False)    
        self.add_line(f"              *****                   |Resolution: {cpuresinfo}", auto_scroll=False)
        self.add_line(f"             *******                  |Shell: {shell}", auto_scroll=False)
        self.update_line("System: ", cheksys or "N/A", 'highlight')
        self.add_line(f"           ***********                |Temp: {temperature}° (outdoor)", auto_scroll=False)
        # self.add_line(f"          *************               |Memory: {mem_used:.1f}GB / {mem_total:.1f}GB", auto_scroll=False)
        self.update_line(f"MEM: ", monitor_memory() or "N/A", 'highlight')
        self.add_line(f"         ***************              |CPU: {cpu_info}, {cpu_temp}", auto_scroll=False)
        self.add_line(f"        *****************             |GPU: {gpu_info}", auto_scroll=False)
        self.add_line(f"                                      |Proxy: {proxy_tf}", 'network', auto_scroll=False)
        self.add_line(f"                                      |IP Address: {ip_address}", 'network', auto_scroll=False)
        self.update_line("Network name: ", self.get_network_name() or "N/A", 'highlight')
        
    
    def get_ip_address(self):
        try:
            if platform.system() == "Windows":
                return subprocess.getoutput("ipconfig | findstr IPv4").split(":")[1].strip()
            else:  
                return subprocess.getoutput("hostname -I").split()[0].strip()
        except:
            return "Unknown"
    
    def get_network_name(self):
        try:
            wifi_info = subprocess.getoutput("netsh wlan show interfaces | findstr SSID")
            return wifi_info.split(":")[1].strip()[:-5] if "SSID" in wifi_info else "N/A"
        except:
            return "N/A"
    
    def setup_timers(self):
        # Настройка всех таймеров обновления
        self.update_clock()
        self.update_ip_name()
        self.update_system_info()
        self.update_memory_inf()
    
    def update_clock(self):
        self.update_line("Time: ", QDateTime.currentDateTime().toString("HH:mm:ss"), 'time')
        QTimer.singleShot(1000, self.update_clock)
    
    def update_ip_name(self):
        self.update_line("Network name: ", self.get_network_name() or "N/A", 'time')
        QTimer.singleShot(64000, self.update_ip_name)
        
    def update_system_info(self):
        self.update_line("System: ", check_inf_windows() or "N/A")
        QTimer.singleShot(64000, self.update_system_info)
        
    def update_memory_inf(self):
        self.update_line("MEM: ", monitor_memory() or "N/A")
        QTimer.singleShot(5000, self.update_memory_inf)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    main_window = QMainWindow()
    main_window.setWindowFlags(Qt.FramelessWindowHint)
    main_window.resize(1000, 415)
    main_window.setStyleSheet("QMainWindow { background: #000000; }")
    
    title_bar = CustomTitleBar(main_window)
    container = QWidget()
    container.setStyleSheet(WINDOW_STYLE)
    
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(title_bar)
    
    terminal = ArchTerminal()
    layout.addWidget(terminal)
    
    main_window.setCentralWidget(container)
    
    def move_window(event):
        if event.buttons() == Qt.LeftButton:
            main_window.move(event.globalPos() - title_bar.drag_pos)
    
    def mouse_press_event(event):
        if event.button() == Qt.LeftButton:
            title_bar.drag_pos = event.globalPos() - main_window.frameGeometry().topLeft()
    
    title_bar.mouseMoveEvent = move_window
    title_bar.mousePressEvent = mouse_press_event
    
    main_window.show()
    sys.exit(app.exec_())
