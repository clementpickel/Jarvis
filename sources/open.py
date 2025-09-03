import subprocess
import winreg
import os

class Open():
    installed_apps = []

    def __init__(self):
        self.installed_apps = self.get_installed_apps()

    def open_calc(self):
        subprocess.Popen("calc.exe")

    def open_word(self):
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")


    def open_excel(self):
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE")

    def open_powerpoint(self):
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE")

    def open_brave(self, url="google.com"):
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        subprocess.Popen([brave_path, url])

    def open_file(self, path):
        os.startfile(path)

    def get_installed_apps(self):
        apps = []
    
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for path in registry_paths:
                try:
                    key = winreg.OpenKey(root, path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        sub_key_name = winreg.EnumKey(key, i)
                        sub_key = winreg.OpenKey(key, sub_key_name)
                        try:
                            app_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                            apps.append(app_name)
                        except FileNotFoundError:
                            continue
                except FileNotFoundError:
                    continue

        ignore_prefixes = ["Microsoft", "NVIDIA", "AMD", "Python", "Windows", "ASUS"]

        filtered_apps = [app for app in apps if not any(app.startswith(prefix) for prefix in ignore_prefixes)]



        return sorted(set(filtered_apps))

        

if __name__ == "__main__":
    # apps = get_installed_apps()
    # for app in apps:
    #     print(app)
    open_client = Open()
    open_client.open_file(r"C:\Users\cpick\Pictures\rplace.png")
