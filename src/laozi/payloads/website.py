import webbrowser


def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
