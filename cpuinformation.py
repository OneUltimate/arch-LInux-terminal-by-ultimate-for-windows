
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
                print(f"{sensor.Name}: {sensor.Value} °C")
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
        used_gb = memory.used / 1024 / 1024
        total_gb = memory.total / (1024 ** 3)
        percent = memory.percent 
            
    
        rez = str(round(used_gb)) + "/" + str(round(total_gb))
        return str(rez)
        
    except:
        return 'n/a'


