import os
import platform
import sys


def set_power_options(option):
    system = platform.system().lower()

    if option == "shutdown":
        if system == "windows":
            os.system("shutdown /s /t 0")
        elif system == "darwin":
            os.system("sudo shutdown -h now")
        elif system == "linux":
            os.system("shutdown now")
        else:
            raise ValueError("Unsupported operating system")

    elif option == "reboot":
        if system == "windows":
            os.system("shutdown /r /t 0")
        elif system == "darwin":
            os.system("sudo shutdown -r now")
        elif system == "linux":
            os.system("reboot")
        else:
            raise ValueError("Unsupported operating system")

    elif option == "logout":
        if system == "windows":
            os.system("shutdown /l")
        elif system == "darwin":
            os.system("osascript -e 'tell application \"System Events\" to log out'")
        elif system == "linux":
            desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
            if "gnome" in desktop_env or "unity" in desktop_env:
                os.system("gnome-session-quit --logout --no-prompt")
            elif "kde" in desktop_env:
                os.system("qdbus org.kde.ksmserver /KSMServer logout 0 0 0")
            else:
                os.system("logout")
        else:
            raise ValueError("Unsupported operating system")

    else:
        raise ValueError("Invalid option. Choose 'shutdown', 'reboot', or 'logout'.")
