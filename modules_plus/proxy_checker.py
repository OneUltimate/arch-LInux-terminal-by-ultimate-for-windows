
import winreg

def get_system_proxy():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings") as key:
            proxy_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
            proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
            if proxy_enable:
                if proxy_server == '127.0.0.1:8888': #измените в зависимости от своих настроек прокси #change according to your proxy settings
                    return 'True ' + str(f'{proxy_server} - local' )
                
                return 'True ' + str(f'{proxy_server}')
            else:
                return 'False'
    except Exception as e:
        print(f"Ошибка при чтении реестра: {e}")

