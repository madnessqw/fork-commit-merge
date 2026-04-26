# System Info Tool v1.0

A comprehensive system information reporter for developers and system administrators. Pure Python, zero dependencies.

## Features

- **CPU Information** - Model, architecture, core count, load average
- **Memory Stats** - Total, used, available, cached memory
- **Disk Usage** - All mounted partitions with usage percentages
- **Network Info** - Interface names and IP addresses
- **OS Details** - Distribution, kernel version, uptime, Python version
- **Export Options** - JSON or Markdown formatted reports

## Usage

```bash
# Display summary
python system_info_tool.py

# Export as JSON
python system_info_tool.py --export json

# Export as Markdown report
python system_info_tool.py --export markdown
```

## Example Output

```
============================================================
  System Info Tool v1.0
  Comprehensive system information reporter
============================================================

📊 SYSTEM SUMMARY
------------------------------------------------------------

🖥️  OS: Linux 5.15.0
   Platform: Linux-5.15.0-x86_64-with-glibc2.35
   Hostname: myserver
   Uptime: 15 days, 8:42:15

⚙️  CPU: Intel(R) Core(TM) i7-9750H
   Architecture: x86_64
   Cores: 12

💾 Memory:
   Total: 31.2 GB
   Available: 18.5 GB

💿 Disks: 3 filesystems mounted

🌐 Network: 2 interfaces
   eth0: 192.168.1.100
   lo: 127.0.0.1
```

## Use Cases

- **Server Documentation** - Generate system specs for documentation
- **Debugging** - Quick system overview when troubleshooting
- **Inventory** - Track hardware across multiple machines
- **Reporting** - Create markdown reports for stakeholders

## Requirements

- Python 3.6+
- Linux (uses /proc filesystem)

## License

MIT - Free for personal and commercial use
