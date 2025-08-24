
from winreg import *
import wmi
import psutil
import os
import time

aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
aKey = OpenKey(aReg, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
nameCPU = QueryValueEx(aKey, 'ProcessorNameString')[0]

w = wmi.WMI(namespace="root\OpenHardwareMonitor")

def cputemp():
    try:
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                
                sensorV = str(round(sensor.Value)) + '°'
                return sensorV
    except:
        return 'N/A'
    
def cputempfortg():
    try:
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                
                sensorV = str(round(sensor.Value)) + '°'
                
                return sensorV
                
    except:
        return 'N/A'
    
def get_gpu_info():
    w = wmi.WMI()
    for gpu in w.Win32_VideoController():       
        return gpu.Name

def get_gpu_info_resolution():
    w = wmi.WMI()
    for gpu in w.Win32_VideoController():
        resslution = str(gpu.CurrentHorizontalResolution) + 'x' + str(gpu.CurrentVerticalResolution)
        return resslution

def monitor_memory():
    try:
        memory = psutil.virtual_memory()
        
        used_mb = memory.used / (1024 ** 2)
        total_mb = memory.total / (1024 ** 2)
        
        percent = memory.percent
        used_mb_rounded = round(used_mb)
        
        total_mb_rounded = round(total_mb)
        bar_length = 10  
        
        filled_length = int(round(bar_length * percent / 100))
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        result = f"[{bar}] {percent}% " #({used_mb_rounded}MB/{total_mb_rounded}MB)
        
        return result
        
    except Exception as e:
        print(f"Error in monitor_memory: {e}")
        return '[░░░░░░░░░░] N/A'

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        return str(f'{battery.percent} %')
    except:
        return 'N/A'

