#!/usr/bin/env python3
"""
Smart URL Shortener - A powerful CLI tool for shortening and managing URLs
Author: UniverseCreator
Version: 1.0.0
License: MIT
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from urllib.parse import urlparse

# Database file for storing URL mappings
DB_FILE = os.path.expanduser("~/.url_shortener_db.json")

# Base62 characters for short code generation
BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def encode_base62(num: int) -> str:
    """Encode a number to base62 string."""
    if num == 0:
        return BASE62[0]
    result = []
    while num > 0:
        result.append(BASE62[num % 62])
        num //= 62
    return ''.join(reversed(result))


def generate_short_code(url: str, length: int = 6) -> str:
    """Generate a unique short code for a URL."""
    # Use hash of URL + timestamp for uniqueness
    hash_input = f"{url}{datetime.now().isoformat()}"
    hash_obj = hashlib.md5(hash_input.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    return encode_base62(hash_int)[:length]


def load_database() -> dict:
    """Load URL database from file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_database(db: dict) -> None:
    """Save URL database to file."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)


def validate_url(url: str) -> bool:
    """Validate if string is a proper URL."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False


def shorten_url(url: str, custom_code: str = None) -> str:
    """Shorten a URL and return the short code."""
    if not validate_url(url):
        raise ValueError(f"Invalid URL: {url}")
    
    db = load_database()
    
    # Check if URL already exists
    for code, data in db.items():
        if data['url'] == url:
            return code
    
    # Generate or use custom short code
    if custom_code:
        if custom_code in db:
            raise ValueError(f"Custom code '{custom_code}' already exists")
        short_code = custom_code
    else:
        short_code = generate_short_code(url)
        while short_code in db:
            short_code = generate_short_code(url + short_code)
    
    # Store in database
    db[short_code] = {
        'url': url,
        'created': datetime.now().isoformat(),
        'clicks': 0
    }
    save_database(db)
    
    return short_code


def expand_url(short_code: str) -> str:
    """Expand a short code to the original URL."""
    db = load_database()
    
    if short_code not in db:
        raise ValueError(f"Short code '{short_code}' not found")
    
    # Increment click counter
    db[short_code]['clicks'] += 1
    db[short_code]['last_accessed'] = datetime.now().isoformat()
    save_database(db)
    
    return db[short_code]['url']


def get_url_info(short_code: str) -> dict:
    """Get information about a shortened URL."""
    db = load_database()
    
    if short_code not in db:
        raise ValueError(f"Short code '{short_code}' not found")
    
    return db[short_code]


def list_urls() -> list:
    """List all shortened URLs."""
    db = load_database()
    return [
        {
            'code': code,
            'url': data['url'],
            'clicks': data['clicks'],
            'created': data['created']
        }
        for code, data in db.items()
    ]


def delete_url(short_code: str) -> bool:
    """Delete a shortened URL."""
    db = load_database()
    
    if short_code not in db:
        raise ValueError(f"Short code '{short_code}' not found")
    
    del db[short_code]
    save_database(db)
    return True


def export_to_html(output_file: str = "url_shortener_export.html") -> str:
    """Export all URLs to an HTML file."""
    urls = list_urls()
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener Export</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .code {{ font-family: monospace; background: #e3f2fd; padding: 4px 8px; border-radius: 4px; }}
        .url {{ color: #666; font-size: 0.9em; }}
        .stats {{ margin-top: 20px; color: #666; }}
    </style>
</head>
<body>
    <h1>🔗 URL Shortener Export</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table>
        <tr>
            <th>Short Code</th>
            <th>Original URL</th>
            <th>Clicks</th>
            <th>Created</th>
        </tr>
"""
    
    for url_data in urls:
        html_content += f"""
        <tr>
            <td><span class="code">{url_data['code']}</span></td>
            <td class="url">{url_data['url']}</td>
            <td>{url_data['clicks']}</td>
            <td>{url_data['created'][:10]}</td>
        </tr>
"""
    
    html_content += f"""
    </table>
    <div class="stats">
        <p>Total URLs: {len(urls)}</p>
        <p>Total Clicks: {sum(u['clicks'] for u in urls)}</p>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    return os.path.abspath(output_file)


def interactive_mode():
    """Run interactive mode."""
    print("=" * 50)
    print("  🔗 Smart URL Shortener - Interactive Mode")
    print("=" * 50)
    print()
    
    while True:
        print("\nOptions:")
        print("  1. Shorten a URL")
        print("  2. Expand a short code")
        print("  3. Get URL info")
        print("  4. List all URLs")
        print("  5. Delete a URL")
        print("  6. Export to HTML")
        print("  7. Exit")
        print()
        
        choice = input("Select option (1-7): ").strip()
        
        if choice == '1':
            url = input("Enter URL to shorten: ").strip()
            custom = input("Custom short code (optional, press Enter to skip): ").strip()
            try:
                code = shorten_url(url, custom if custom else None)
                print(f"\n✅ URL shortened!")
                print(f"   Short code: {code}")
                print(f"   Full short URL: http://short.link/{code}")
            except ValueError as e:
                print(f"\n❌ Error: {e}")
        
        elif choice == '2':
            code = input("Enter short code: ").strip()
            try:
                url = expand_url(code)
                print(f"\n✅ Expanded URL: {url}")
            except ValueError as e:
                print(f"\n❌ Error: {e}")
        
        elif choice == '3':
            code = input("Enter short code: ").strip()
            try:
                info = get_url_info(code)
                print(f"\n📊 URL Info:")
                print(f"   Original URL: {info['url']}")
                print(f"   Clicks: {info['clicks']}")
                print(f"   Created: {info['created']}")
                if 'last_accessed' in info:
                    print(f"   Last accessed: {info['last_accessed']}")
            except ValueError as e:
                print(f"\n❌ Error: {e}")
        
        elif choice == '4':
            urls = list_urls()
            if not urls:
                print("\n📭 No URLs found.")
            else:
                print(f"\n📋 All URLs ({len(urls)} total):")
                print("-" * 80)
                for u in urls:
                    print(f"  {u['code']:10} → {u['url'][:50]:50} ({u['clicks']} clicks)")
        
        elif choice == '5':
            code = input("Enter short code to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{code}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                try:
                    delete_url(code)
                    print(f"\n✅ URL '{code}' deleted.")
                except ValueError as e:
                    print(f"\n❌ Error: {e}")
            else:
                print("\nCancelled.")
        
        elif choice == '6':
            filename = input("Output filename (default: url_shortener_export.html): ").strip()
            if not filename:
                filename = "url_shortener_export.html"
            try:
                path = export_to_html(filename)
                print(f"\n✅ Exported to: {path}")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option. Please select 1-7.")


def main():
    parser = argparse.ArgumentParser(
        description="Smart URL Shortener - Shorten and manage URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i                    # Interactive mode
  %(prog)s -u https://example.com           # Shorten URL
  %(prog)s -u https://example.com -c mylink # Shorten with custom code
  %(prog)s -e abc123             # Expand short code
  %(prog)s -l                    # List all URLs
  %(prog)s --export              # Export to HTML
        """
    )
    
    parser.add_argument('-u', '--url', help='URL to shorten')
    parser.add_argument('-c', '--custom', help='Custom short code')
    parser.add_argument('-e', '--expand', help='Expand short code to URL')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('-l', '--list', action='store_true', help='List all URLs')
    parser.add_argument('--info', help='Get info about short code')
    parser.add_argument('-d', '--delete', help='Delete short code')
    parser.add_argument('--export', action='store_true', help='Export to HTML')
    parser.add_argument('--db-location', action='store_true', help='Show database file location')
    
    args = parser.parse_args()
    
    try:
        if args.db_location:
            print(f"Database location: {DB_FILE}")
        
        elif args.interactive:
            interactive_mode()
        
        elif args.url:
            code = shorten_url(args.url, args.custom)
            print(f"Shortened URL: {code}")
            print(f"Full URL: http://short.link/{code}")
        
        elif args.expand:
            url = expand_url(args.expand)
            print(f"Original URL: {url}")
        
        elif args.list:
            urls = list_urls()
            if not urls:
                print("No URLs found.")
            else:
                print(f"\n{'Code':<12} {'Clicks':<8} {'URL':<50}")
                print("-" * 70)
                for u in urls:
                    print(f"{u['code']:<12} {u['clicks']:<8} {u['url'][:50]:<50}")
        
        elif args.info:
            info = get_url_info(args.info)
            print(f"Code: {args.info}")
            print(f"URL: {info['url']}")
            print(f"Clicks: {info['clicks']}")
            print(f"Created: {info['created']}")
            if 'last_accessed' in info:
                print(f"Last accessed: {info['last_accessed']}")
        
        elif args.delete:
            delete_url(args.delete)
            print(f"Deleted: {args.delete}")
        
        elif args.export:
            path = export_to_html()
            print(f"Exported to: {path}")
        
        else:
            parser.print_help()
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(0)


if __name__ == '__main__':
    main()
