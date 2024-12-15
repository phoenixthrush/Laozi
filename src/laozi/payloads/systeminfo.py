import platform
from datetime import datetime

import psutil


def get_sys_info():
    details = []

    system_info = platform.uname()
    details.append(f"{'='*20} System Details {'='*20}")
    details.append(f"OS: {system_info.system}")
    details.append(f"Host Name: {system_info.node}")
    details.append(f"OS Release: {system_info.release}")
    details.append(f"OS Version: {system_info.version}")
    details.append(f"Architecture: {system_info.machine}")
    details.append(f"Processor: {system_info.processor}")

    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp)
    details.append(f"{'='*20} Boot Details {'='*20}")
    details.append(f"Boot Time: {boot_time.strftime('%Y/%m/%d %H:%M:%S')}")

    details.append(f"{'='*20} CPU Details {'='*20}")
    details.append(f"Physical Cores: {psutil.cpu_count(logical=False)}")
    details.append(f"Logical Cores: {psutil.cpu_count(logical=True)}")
    cpu_freq = psutil.cpu_freq()
    details.append(f"Max Frequency: {cpu_freq.max:.2f} MHz")
    details.append(f"Min Frequency: {cpu_freq.min:.2f} MHz")
    details.append(f"Current Frequency: {cpu_freq.current:.2f} MHz")
    details.append("Per-Core Usage:")
    for idx, usage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        details.append(f"  Core {idx}: {usage}%")
    details.append(f"Total CPU Usage: {psutil.cpu_percent()}%")

    memory = psutil.virtual_memory()
    details.append(f"{'='*20} Memory Details {'='*20}")
    details.append(f"Total: {_format_size(memory.total)}")
    details.append(f"Available: {_format_size(memory.available)}")
    details.append(f"Used: {_format_size(memory.used)}")
    details.append(f"Usage Percentage: {memory.percent}%")

    swap_memory = psutil.swap_memory()
    details.append(f"{'='*20} Swap Details {'='*20}")
    details.append(f"Total: {_format_size(swap_memory.total)}")
    details.append(f"Free: {_format_size(swap_memory.free)}")
    details.append(f"Used: {_format_size(swap_memory.used)}")
    details.append(f"Usage Percentage: {swap_memory.percent}%")

    details.append(f"{'='*20} Disk Details {'='*20}")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        details.append(f"=== Partition: {partition.device} ===")
        details.append(f"  Mount Point: {partition.mountpoint}")
        details.append(f"  File System: {partition.fstype}")
        details.append(f"  Total Size: {_format_size(usage.total)}")
        details.append(f"  Used: {_format_size(usage.used)}")
        details.append(f"  Free: {_format_size(usage.free)}")
        details.append(f"  Usage Percentage: {usage.percent}%")

    disk_io_stats = psutil.disk_io_counters()
    details.append(f"Disk Read: {_format_size(disk_io_stats.read_bytes)}")
    details.append(f"Disk Write: {_format_size(disk_io_stats.write_bytes)}")

    network_interfaces = psutil.net_if_addrs()
    details.append(f"{'='*20} Network Details {'='*20}")
    for interface, addresses in network_interfaces.items():
        details.append(f"=== Interface: {interface} ===")
        for addr in addresses:
            if addr.family.name == 'AF_INET':
                details.append(f"  IPv4 Address: {addr.address}")
                details.append(f"  Netmask: {addr.netmask}")
                details.append(f"  Broadcast: {addr.broadcast}")
            elif addr.family.name == 'AF_PACKET':
                details.append(f"  MAC Address: {addr.address}")
                details.append(f"  Netmask: {addr.netmask}")
                details.append(f"  Broadcast MAC: {addr.broadcast}")

    network_stats = psutil.net_io_counters()
    details.append(f"Data Sent: {_format_size(network_stats.bytes_sent)}")
    details.append(f"Data Received: {_format_size(network_stats.bytes_recv)}")

    return "\n".join(details)


def _format_size(bytes, unit_suffix="B"):
    unit_scale = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < unit_scale:
            return f"{bytes:.2f}{unit}{unit_suffix}"
        bytes /= unit_scale


if __name__ == '__main__':
    print(get_sys_info())
