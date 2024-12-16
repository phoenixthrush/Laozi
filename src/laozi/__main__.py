import os
from discord import Intents
from .bot import DiscordBotClient


def load_environment_variables(file_path="../.env"):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


if __name__ == '__main__':
    load_environment_variables()
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = int(os.getenv("CHANNEL_ID"))

    intents = Intents.default()
    intents.message_content = True

    bot = DiscordBotClient(channel_id, intents=intents)
    bot.run(bot_token)
