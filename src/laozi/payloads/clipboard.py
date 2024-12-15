import pyperclip


def get_clipboard():
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as e:
        return f"Clipboard access failed: {str(e)}"
