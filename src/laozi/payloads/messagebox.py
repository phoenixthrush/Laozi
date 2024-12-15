import platform
import subprocess


def display_messagebox(message, title="Message", message_type="info"):
    system = platform.system()

    if system == "Windows":
        return _windows_messagebox_response(message, title, message_type)

    if system == "Darwin":
        return _macos_messagebox_response(message, title, message_type)

    if system == "Linux":
        return _linux_messagebox_response(message, title, message_type)

    return _fallback_messagebox_response(message, title, message_type)


def _windows_messagebox_response(message, title, message_type):
    import ctypes

    messagebox_types = {
        "info": 0x40,
        "yesno": 0x04 | 0x20,
        "warning": 0x30,
        "error": 0x10,
    }

    box_type = messagebox_types.get(message_type, 0x40)
    response = ctypes.windll.user32.MessageBoxW(0, message, title, box_type)
    return response == 6 if message_type == "yesno" else True


def _macos_messagebox_response(message, title, message_type):
    applescript_templates = {
        "info": f'display dialog "{message}" with title "{title}" buttons "OK"',
        "yesno": f'display dialog "{message}" with title "{title}" buttons {"Yes", "No"}',
        "warning": f'display dialog "{message}" with title "{title}" buttons "OK" with icon caution',
        "error": f'display dialog "{message}" with title "{title}" buttons "OK" with icon stop',
    }

    script = applescript_templates.get(message_type,
                                       f'display dialog "{message}" with title "{title}" buttons "OK"')

    try:
        result = subprocess.run(["osascript", "-e", script], text=True, capture_output=True, check=False)
        return "Yes" in result.stdout if message_type == "yesno" else True
    except subprocess.SubprocessError as error:
        print(f"Error displaying messagebox on macOS: {error}")
        return False


def _linux_messagebox_response(message, title, message_type):
    dialog_tool = "zenity" if _is_tool_available("zenity") else "kdialog"

    commands = {
        "zenity": {
            "info": ["zenity", "--info", "--text", message, "--title", title],
            "yesno": ["zenity", "--question", "--text", message, "--title", title],
            "warning": ["zenity", "--warning", "--text", message, "--title", title],
            "error": ["zenity", "--error", "--text", message, "--title", title],
        },
        "kdialog": {
            "info": ["kdialog", "--msgbox", message, "--title", title],
            "yesno": ["kdialog", "--yesno", message, "--title", title],
            "warning": ["kdialog", "--sorry", message, "--title", title],
            "error": ["kdialog", "--error", message, "--title", title],
        },
    }

    command = commands.get(dialog_tool, {}).get(message_type, commands["zenity"]["info"])

    try:
        result = subprocess.run(command, check=False)
        return result.returncode == 0 if message_type == "yesno" else True
    except subprocess.SubprocessError as error:
        print(f"Error displaying messagebox on Linux: {error}")
        return False


def _fallback_messagebox_response(message, title, message_type):
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()

    if message_type == "yesno":
        return messagebox.askyesno(title, message)
    elif message_type == "warning":
        messagebox.showwarning(title, message)
    elif message_type == "error":
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)
    return True


def _is_tool_available(tool_name):
    return subprocess.run(["which", tool_name], capture_output=True, text=True, check=False).returncode == 0


if __name__ == '__main__':
    display_messagebox("Test", "Test", "info")
