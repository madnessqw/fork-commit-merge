#!/usr/bin/env python3
"""
Log Analyzer CLI - Parse, analyze, and visualize log files
Quickly identify errors, patterns, and anomalies in your logs
"""

import argparse
import re
import sys
import json
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path

__version__ = "1.0.0"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze log files and extract insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s app.log                    # Basic analysis
  %(prog)s app.log --errors-only      # Show only errors
  %(prog)s app.log --pattern "ERROR"  # Find specific pattern
  %(prog)s app.log --json             # Output as JSON
  %(prog)s app.log --real-time        # Follow log in real-time
        """
    )
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("--errors-only", "-e", action="store_true",
                       help="Show only error entries")
    parser.add_argument("--pattern", "-p", help="Search for specific pattern")
    parser.add_argument("--level", "-l", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                       help="Filter by log level")
    parser.add_argument("--since", help="Show entries since datetime (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--until", help="Show entries until datetime (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--top", "-t", type=int, default=10,
                       help="Show top N frequent messages (default: 10)")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output results as JSON")
    parser.add_argument("--real-time", "-f", action="store_true",
                       help="Follow log file in real-time (like tail -f)")
    parser.add_argument("--export", "-x", help="Export results to file")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args()


def parse_log_line(line):
    """Parse a log line and extract structured data"""
    patterns = [
        # Standard Python logging format
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+-\s+(?P<level>\w+)\s+-\s+(?P<message>.*)',
        # Common web server format
        r'(?P<ip>\d+\.\d+\.\d+\.\d+).*\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<path>[^\s]+)"\s+(?P<status>\d+)',
        # Simple timestamp format
        r'\[(?P<timestamp>[^\]]+)\]\s+(?P<level>\w+):?\s*(?P<message>.*)',
        # Syslog format
        r'(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<message>.*)',
    ]

    for pattern in patterns:
        match = re.match(pattern, line.strip())
        if match:
            return match.groupdict()

    return {"raw": line.strip()}


def analyze_log_file(filepath, args):
    """Analyze log file and return statistics"""
    stats = {
        "total_lines": 0,
        "levels": Counter(),
        "errors": [],
        "hourly_distribution": defaultdict(int),
        "unique_messages": Counter(),
        "ips": Counter(),
        "status_codes": Counter(),
        "patterns_found": []
    }

    since_dt = datetime.strptime(args.since, "%Y-%m-%d %H:%M:%S") if args.since else None
    until_dt = datetime.strptime(args.until, "%Y-%m-%d %H:%M:%S") if args.until else None

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                stats["total_lines"] += 1
                parsed = parse_log_line(line)

                # Filter by level
                if args.level and parsed.get("level") != args.level:
                    continue

                # Filter by pattern
                if args.pattern and args.pattern not in line:
                    continue

                # Collect errors
                level = parsed.get("level", "UNKNOWN")
                if level in ["ERROR", "CRITICAL", "FATAL"] or args.errors_only:
                    stats["errors"].append({
                        "line": line_num,
                        "content": line.strip(),
                        "parsed": parsed
                    })

                stats["levels"][level] += 1

                # Hourly distribution
                timestamp = parsed.get("timestamp", "")
                if timestamp:
                    try:
                        if ' ' in timestamp:
                            hour = timestamp.split()[1].split(':')[0]
                            stats["hourly_distribution"][f"{hour}:00"] += 1
                    except:
                        pass

                # Unique messages (simplified)
                message = parsed.get("message", parsed.get("raw", ""))
                if message:
                    # Normalize message by removing variable parts
                    normalized = re.sub(r'\d+', 'N', message[:100])
                    stats["unique_messages"][normalized] += 1

                # IP addresses (for web logs)
                ip = parsed.get("ip")
                if ip:
                    stats["ips"][ip] += 1

                # HTTP status codes
                status = parsed.get("status")
                if status:
                    stats["status_codes"][status] += 1

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{filepath}'", file=sys.stderr)
        sys.exit(1)

    return stats


def print_analysis(stats, args):
    """Print formatted analysis results"""
    if args.json:
        print(json.dumps(stats, indent=2, default=str))
        return

    print("=" * 60)
    print("LOG ANALYSIS REPORT")
    print("=" * 60)
    print(f"Total lines analyzed: {stats['total_lines']}")
    print()

    # Log levels
    if stats["levels"]:
        print("LOG LEVELS:")
        print("-" * 40)
        for level, count in stats["levels"].most_common():
            percentage = (count / stats["total_lines"]) * 100
            bar = "█" * int(percentage / 2)
            print(f"  {level:12} {count:6} ({percentage:5.1f}%) {bar}")
        print()

    # Errors
    if stats["errors"]:
        print(f"ERRORS FOUND: {len(stats['errors'])}")
        print("-" * 40)
        for error in stats["errors"][:20]:  # Show first 20
            print(f"  Line {error['line']}: {error['content'][:80]}...")
        if len(stats["errors"]) > 20:
            print(f"  ... and {len(stats['errors']) - 20} more errors")
        print()

    # Top messages
    if stats["unique_messages"]:
        print(f"TOP {args.top} FREQUENT MESSAGES:")
        print("-" * 40)
        for msg, count in stats["unique_messages"].most_common(args.top):
            print(f"  {count:4}x  {msg[:60]}...")
        print()

    # Hourly distribution
    if stats["hourly_distribution"]:
        print("HOURLY DISTRIBUTION:")
        print("-" * 40)
        for hour, count in sorted(stats["hourly_distribution"].items()):
            bar = "█" * (count // max(stats["hourly_distribution"].values()) * 30 + 1)
            print(f"  {hour}  {count:4} {bar}")
        print()

    # IP addresses
    if stats["ips"]:
        print("TOP IP ADDRESSES:")
        print("-" * 40)
        for ip, count in stats["ips"].most_common(10):
            print(f"  {ip:20} {count:6}")
        print()

    # Status codes
    if stats["status_codes"]:
        print("HTTP STATUS CODES:")
        print("-" * 40)
        for status, count in stats["status_codes"].most_common():
            print(f"  {status:6} {count:6}")
        print()

    print("=" * 60)


def follow_log(filepath, args):
    """Follow log file in real-time"""
    print(f"Following {filepath}... (Press Ctrl+C to stop)")
    print("-" * 60)

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            # Go to end of file
            f.seek(0, 2)

            while True:
                line = f.readline()
                if not line:
                    import time
                    time.sleep(0.1)
                    continue

                # Apply filters
                if args.level and args.level not in line:
                    continue
                if args.pattern and args.pattern not in line:
                    continue
                if args.errors_only and not any(lvl in line for lvl in ["ERROR", "CRITICAL", "FATAL"]):
                    continue

                print(line.strip())

    except KeyboardInterrupt:
        print("\nStopped following log file.")


def export_results(stats, filepath):
    """Export analysis results to file"""
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "analysis": stats
    }

    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)

    print(f"Results exported to: {filepath}")


def main():
    args = parse_args()

    if args.real_time:
        follow_log(args.logfile, args)
    else:
        stats = analyze_log_file(args.logfile, args)
        print_analysis(stats, args)

        if args.export:
            export_results(stats, args.export)


if __name__ == "__main__":
    main()
