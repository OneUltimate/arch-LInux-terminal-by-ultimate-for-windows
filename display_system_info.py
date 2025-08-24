import platform
import psutil
import datetime
import time
import subprocess
import os
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import (
    QTimer, QDateTime, Qt, QProcess,)

from data.modules_plus.cheking_system import check_inf_windows
from data.modules_plus.pc_information import (cputemp, cputempfortg, get_gpu_info, get_battery_info, 
                                         get_gpu_info_resolution, monitor_memory, nameCPU)
from data.modules_plus.proxy_checker import get_system_proxy
from data.modules_plus.weather import temp1


class SystemInfoDisplay:
    def __init__(self, arch_terminal, colors):
        self.arch_terminal = arch_terminal 
        self.colors = colors
    
    def display_system_info(self):
        
        self.arch_terminal.terminal.clear()  
        
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
        mem_total = mem.total / (1024**3) 
        
        cpu_info = str(nameCPU[:-2])
        gpu_info = get_gpu_info()
        
        cpu_temp = cputemp()
        temperature = temp1()
        ip_address = self.get_ip_address()
        cpuresinfo = get_gpu_info_resolution()
        cheksys = check_inf_windows()
        proxy_tf = get_system_proxy()
        battery_info = get_battery_info()
        
        self.arch_terminal.add_line("--------------------------------", 'highlight')
        self.arch_terminal.add_line(f'{os_info}', auto_scroll=False)
        self.arch_terminal.add_line(f'{kernel}', auto_scroll=False)
       
        self.arch_terminal.update_line("Time: ", QDateTime.currentDateTime().toString("HH:mm:ss"), 'time')
        self.arch_terminal.update_line("System: ", cheksys or "N/A", 'highlight')
        self.arch_terminal.add_line(f"           /\     ┌──┐      ┌─┐       |Uptime: {uptime_str}", auto_scroll=False)
        self.arch_terminal.add_line(f"          /  \    |  |      | |       |Host: {platform.node()}, {battery_info}", auto_scroll=False)    
        self.arch_terminal.add_line(f"         / /\ \   |  |      | |       |Resolution: {cpuresinfo}", auto_scroll=False)
        self.arch_terminal.add_line(f"        / /  \ \  |  |      | |       |Shell: {shell}", auto_scroll=False)
        self.arch_terminal.add_line(f"       /  \__/  \ |  |      | |       |Temp: {temperature}° (outdoor)", auto_scroll=False)
        self.arch_terminal.add_line(f"      /  /\  /\  \|  |______| |       |CPU: {cpu_info}, {cpu_temp}", auto_scroll=False)
        self.arch_terminal.add_line(f"     /__/  \/  \__\___________|       |GPU: {gpu_info}", auto_scroll=False)
        self.arch_terminal.update_line(f"MEM: ", monitor_memory() or "N/A", 'highlight')
        self.arch_terminal.add_line(f"                                      |Proxy: {proxy_tf}", 'network', auto_scroll=False)
        self.arch_terminal.add_line(f"prealpha-08                           |IP Address: {ip_address}", 'network', auto_scroll=False)
        self.arch_terminal.update_line("Network name: ", self.get_network_name() or "N/A", 'highlight')
    
    def get_ip_address(self):
        try:
            if platform.system() == "Windows":
                return subprocess.getoutput("ipconfig | findstr IPv4").split(":")[1].strip()
            else:  
                return subprocess.getoutput("hostname -I").split()[0].strip()
        except:
            return "N/A"
    
    def get_network_name(self):
        try:
            wifi_info = subprocess.getoutput("netsh wlan show interfaces | findstr SSID")
            return wifi_info.split(":")[1].strip()[:-5] if "SSID" in wifi_info else "N/A"
        except:
            return "N/A"
    
    def setup_timers(self):
        self.update_clock()
        self.update_ip_name()
        self.update_system_info()
        self.update_memory_inf()
    
    def update_clock(self):
        self.arch_terminal.update_line("Time: ", QDateTime.currentDateTime().toString("HH:mm:ss"), 'time')
        QTimer.singleShot(1000, self.update_clock)
    
    def update_ip_name(self):
        self.arch_terminal.update_line("Network name: ", self.get_network_name() or "N/A", 'time')
        QTimer.singleShot(60000, self.update_ip_name)
        
    def update_system_info(self):
        self.arch_terminal.update_line("System: ", check_inf_windows() or "N/A")
        QTimer.singleShot(150000, self.update_system_info)
        
    def update_memory_inf(self):
        self.arch_terminal.update_line("MEM: ", monitor_memory() or "N/A")
        QTimer.singleShot(5000, self.update_memory_inf)