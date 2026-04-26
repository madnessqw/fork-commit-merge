#!/usr/bin/env python3
"""
System Info Tool - Comprehensive system information reporter
A standalone Python script for developers and system administrators

Usage:
    python system_info_tool.py
    python system_info_tool.py --export json
    python system_info_tool.py --export markdown

Features:
    - CPU info (cores, usage, architecture)
    - Memory info (total, used, available)
    - Disk usage (all mounted partitions)
    - Network info (interfaces, IP addresses)
    - OS info (distribution, kernel, uptime)
    - Export to JSON or Markdown
"""

import os
import sys
import platform
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


def get_cpu_info():
    """Get CPU information"""
    info = {
        "processor": platform.processor(),
        "architecture": platform.machine(),
        "cores_physical": os.cpu_count(),
        "cores_logical": os.cpu_count(),  # Same on most systems
    }
    
    # Try to get CPU usage
    try:
        if hasattr(os, 'getloadavg'):
            load1, load5, load15 = os.getloadavg()
            info["load_average"] = {"1min": load1, "5min": load5, "15min": load15}
    except:
        pass
    
    # Try to get more CPU info from /proc on Linux
    if Path("/proc/cpuinfo").exists():
        try:
            with open("/proc/cpuinfo") as f:
                cpuinfo = f.read()
                for line in cpuinfo.split("\n"):
                    if "model name" in line:
                        info["model"] = line.split(":")[1].strip()
                        break
        except:
            pass
    
    return info


def get_memory_info():
    """Get memory information"""
    info = {}
    
    # Linux /proc/meminfo
    if Path("/proc/meminfo").exists():
        try:
            with open("/proc/meminfo") as f:
                meminfo = f.read()
                for line in meminfo.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        info[key.strip().lower()] = value.strip()
        except:
            pass
    
    return info


def get_disk_info():
    """Get disk usage information"""
    disks = []
    
    try:
        # Get all mounted filesystems
        result = subprocess.run(
            ["df", "-h"], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        
        lines = result.stdout.strip().split("\n")[1:]  # Skip header
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                disks.append({
                    "filesystem": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "use_percent": parts[4],
                    "mount": parts[5]
                })
    except:
        pass
    
    return disks


def get_network_info():
    """Get network interface information"""
    interfaces = []
    
    try:
        # Get network interfaces
        result = subprocess.run(
            ["ip", "addr"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        current_iface = None
        for line in result.stdout.split("\n"):
            if line.startswith(" ") and "inet" in line:
                parts = line.strip().split()
                for i, part in enumerate(parts):
                    if part.startswith("inet") and i + 1 < len(parts):
                        ip = parts[i + 1].split("/")[0]
                        if current_iface:
                            interfaces.append({
                                "interface": current_iface,
                                "ip": ip
                            })
            elif line[0].isdigit() and ":" in line:
                current_iface = line.split(":")[1].strip()
    except:
        pass
    
    return interfaces


def get_os_info():
    """Get operating system information"""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "platform": platform.platform(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
    }
    
    # Get distribution info
    if hasattr(platform, 'freedesktop_os_release'):
        try:
            info["distribution"] = platform.freedesktop_os_release()
        except:
            pass
    
    # Get uptime
    if Path("/proc/uptime").exists():
        try:
            with open("/proc/uptime") as f:
                uptime_seconds = float(f.read().split()[0])
                uptime_delta = timedelta(seconds=int(uptime_seconds))
                info["uptime"] = str(uptime_delta)
        except:
            pass
    
    return info


def format_bytes(size_str):
    """Format memory size strings"""
    try:
        size_kb = int(size_str.split()[0])
        if size_kb > 1024 * 1024:
            return f"{size_kb / (1024 * 1024):.2f} GB"
        elif size_kb > 1024:
            return f"{size_kb / 1024:.2f} MB"
        else:
            return f"{size_kb} KB"
    except:
        return size_str


def generate_markdown_report(data):
    """Generate Markdown formatted report"""
    lines = [
        "# System Information Report",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n---\n",
        "## Operating System",
        f"- **System:** {data['os']['system']}",
        f"- **Platform:** {data['os']['platform']}",
        f"- **Hostname:** {data['os']['hostname']}",
        f"- **Python:** {data['os']['python_version']}",
    ]
    
    if 'uptime' in data['os']:
        lines.append(f"- **Uptime:** {data['os']['uptime']}")
    
    lines.extend([
        "\n## CPU",
        f"- **Processor:** {data['cpu'].get('model', data['cpu'].get('processor', 'Unknown'))}",
        f"- **Architecture:** {data['cpu']['architecture']}",
        f"- **Cores:** {data['cpu']['cores_physical']}",
    ])
    
    if 'load_average' in data['cpu']:
        load = data['cpu']['load_average']
        lines.append(f"- **Load Average:** {load['1min']:.2f}, {load['5min']:.2f}, {load['15min']:.2f}")
    
    lines.extend(["\n## Memory"])
    if data['memory']:
        for key, value in data['memory'].items():
            lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
    else:
        lines.append("- Memory information unavailable")
    
    lines.extend(["\n## Disk Usage"])
    if data['disks']:
        lines.append("\n| Filesystem | Size | Used | Available | Use% | Mount |")
        lines.append("|------------|------|------|-----------|------|-------|")
        for disk in data['disks']:
            lines.append(
                f"| {disk['filesystem']} | {disk['size']} | {disk['used']} | "
                f"{disk['available']} | {disk['use_percent']} | {disk['mount']} |"
            )
    else:
        lines.append("- Disk information unavailable")
    
    lines.extend(["\n## Network Interfaces"])
    if data['network']:
        for iface in data['network']:
            lines.append(f"- **{iface['interface']}:** {iface['ip']}")
    else:
        lines.append("- Network information unavailable")
    
    return "\n".join(lines)


def print_summary(data):
    """Print formatted summary to console"""
    print("\n" + "=" * 60)
    print("  System Info Tool v1.0")
    print("  Comprehensive system information reporter")
    print("=" * 60 + "\n")
    
    print("📊 SYSTEM SUMMARY")
    print("-" * 60)
    
    # OS Info
    print(f"\n🖥️  OS: {data['os']['system']} {data['os']['release']}")
    print(f"   Platform: {data['os']['platform']}")
    print(f"   Hostname: {data['os']['hostname']}")
    if 'uptime' in data['os']:
        print(f"   Uptime: {data['os']['uptime']}")
    
    # CPU Info
    cpu_model = data['cpu'].get('model', data['cpu'].get('processor', 'Unknown'))
    print(f"\n⚙️  CPU: {cpu_model}")
    print(f"   Architecture: {data['cpu']['architecture']}")
    print(f"   Cores: {data['cpu']['cores_physical']}")
    if 'load_average' in data['cpu']:
        load = data['cpu']['load_average']
        print(f"   Load: {load['1min']:.2f} {load['5min']:.2f} {load['15min']:.2f}")
    
    # Memory Info
    print(f"\n💾 Memory:")
    if 'memtotal' in data['memory']:
        print(f"   Total: {format_bytes(data['memory']['memtotal'])}")
    if 'memavailable' in data['memory']:
        print(f"   Available: {format_bytes(data['memory']['memavailable'])}")
    
    # Disk Info
    print(f"\n💿 Disks: {len(data['disks'])} filesystems mounted")
    for disk in data['disks'][:3]:  # Show first 3
        print(f"   {disk['mount']}: {disk['used']} / {disk['size']} ({disk['use_percent']})")
    if len(data['disks']) > 3:
        print(f"   ... and {len(data['disks']) - 3} more")
    
    # Network Info
    print(f"\n🌐 Network: {len(data['network'])} interfaces")
    for iface in data['network'][:3]:
        print(f"   {iface['interface']}: {iface['ip']}")
    if len(data['network']) > 3:
        print(f"   ... and {len(data['network']) - 3} more")
    
    print("\n" + "=" * 60 + "\n")


def main():
    """Main entry point"""
    export_format = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--export" and len(sys.argv) > 2:
            export_format = sys.argv[2]
        elif sys.argv[1] in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
    
    # Gather all information
    data = {
        "timestamp": datetime.now().isoformat(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disks": get_disk_info(),
        "network": get_network_info(),
        "os": get_os_info(),
    }
    
    # Export or print
    if export_format == "json":
        print(json.dumps(data, indent=2))
    elif export_format == "markdown":
        print(generate_markdown_report(data))
    else:
        print_summary(data)


if __name__ == "__main__":
    main()