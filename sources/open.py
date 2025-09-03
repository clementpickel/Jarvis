import subprocess

# # Open Calculator
# subprocess.Popen("calc.exe")

# # Open Notepad
# subprocess.Popen("notepad.exe")

# # Open Steam (replace path with your installation path)
subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe")


import winreg

def get_installed_apps():
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

    return sorted(set(filtered_apps))  # Remove duplicates and sort

if __name__ == "__main__":
    apps = get_installed_apps()
    for app in apps:
        print(app)
