import platform
import psutil
import socket
import subprocess
import os
import re


def check_cpu():
    try:
        psutil.cpu_percent(interval=1)
        return 1
    except:
        return 0

def check_ram():
    try:
        psutil.virtual_memory()
        return 1
    except:
        return 0

def check_disk():
    try:
        psutil.disk_usage('C:\\')
        return 1
    except:
        return 0

def check_network():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return 1
    except:
        return 0

def check_wifi():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        if "Состояние" in result.stdout or "State" in result.stdout:  # Для разных языков
            return 1
        return 0
    except:
        return 0

def check_gpu():
    try:
        result = subprocess.run(['dxdiag', '/t', 'dxdiag_temp.txt'], capture_output=True, text=True)
        if result.returncode == 0:
            with open('dxdiag_temp.txt', 'r', encoding='utf-16') as f:
                content = f.read()
                os.remove('dxdiag_temp.txt')
                if "Display Devices" in content:
                    return 1
        return 0
    except:
        return 0

def check_audio():
    try:
        result = subprocess.run(['powershell', 'Get-AudioDevice -Playback'], capture_output=True, text=True)
        return 1 if result.returncode == 0 else 0
    except:
        return 0

def check_os():
    try:
        platform.platform()
        return 1
    except:
        return 0

def check_usb():
    try:
        result = subprocess.run(['powershell', 'Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match "^USB" }'], 
                              capture_output=True, text=True)
        usb_devices = [line for line in result.stdout.split('\n') if line.strip()]
        return 1 if len(usb_devices) > 1 else 0  # Более 1 строки (заголовок + хотя бы одно устройство)
    except:
        return 0



def check_inf_windows():
    check_inf_windows = []
    
    
    
    check_inf_windows += str(check_cpu()) + str(check_ram()) + str(check_disk()) + str(check_network()) + str(check_os()) + str(check_usb())
    
    check_inf_windows = ''.join(check_inf_windows)
    
    
    
    check_inf_windows = check_inf_windows.replace('1', '■')
    check_inf_windows = check_inf_windows.replace('0', ' ')
        
    # print(check_inf_windows)
    
    return check_inf_windows
    

    
if __name__ == "__main__":
    check_inf_windows()
