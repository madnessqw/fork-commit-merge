#!/usr/bin/env python3
"""
GitHub Bounty Hunter CLI
A tool to discover, track, and manage GitHub bounty opportunities
Author: UniverseCreator
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests


class BountyHunter:
    """GitHub Bounty Hunter - Find and track bounty opportunities"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        self.headers['Accept'] = 'application/vnd.github.v3+json'
        
        # Data storage
        self.data_dir = os.path.expanduser('~/.bounty-hunter')
        os.makedirs(self.data_dir, exist_ok=True)
        self.tracked_file = os.path.join(self.data_dir, 'tracked_bounties.json')
        self.stats_file = os.path.join(self.data_dir, 'stats.json')
    
    def _load_tracked(self) -> List[Dict]:
        """Load tracked bounties from disk"""
        if os.path.exists(self.tracked_file):
            with open(self.tracked_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_tracked(self, bounties: List[Dict]):
        """Save tracked bounties to disk"""
        with open(self.tracked_file, 'w') as f:
            json.dump(bounties, f, indent=2)
    
    def _load_stats(self) -> Dict:
        """Load statistics from disk"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {
            'total_searched': 0,
            'total_tracked': 0,
            'completed': 0,
            'earnings': 0.0,
            'first_run': datetime.now().isoformat()
        }
    
    def _save_stats(self, stats: Dict):
        """Save statistics to disk"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def search_bounties(self, query: str = "bounty", language: Optional[str] = None, 
                       min_reward: Optional[float] = None, max_results: int = 30) -> List[Dict]:
        """
        Search for bounty issues on GitHub
        
        Args:
            query: Search query (default: "bounty")
            language: Filter by programming language
            min_reward: Minimum reward amount to filter
            max_results: Maximum number of results
        """
        search_query = f"is:issue is:open label:bounty {query}"
        if language:
            search_query += f" language:{language}"
        
        url = f"{self.base_url}/search/issues"
        params = {
            'q': search_query,
            'sort': 'updated',
            'order': 'desc',
            'per_page': max_results
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            bounties = []
            for item in data.get('items', []):
                bounty = {
                    'id': item['id'],
                    'number': item['number'],
                    'title': item['title'],
                    'url': item['html_url'],
                    'state': item['state'],
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'comments': item['comments'],
                    'repository': item['repository_url'].split('/')[-1],
                    'owner': item['repository_url'].split('/')[-2],
                    'body': item.get('body', '')[:500],  # First 500 chars
                    'labels': [label['name'] for label in item.get('labels', [])]
                }
                
                # Try to extract reward from title/body
                bounty['estimated_reward'] = self._extract_reward(item['title'], item.get('body', ''))
                
                # Filter by minimum reward
                if min_reward and bounty['estimated_reward'] < min_reward:
                    continue
                
                bounties.append(bounty)
            
            # Update stats
            stats = self._load_stats()
            stats['total_searched'] += len(bounties)
            self._save_stats(stats)
            
            return bounties
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching bounties: {e}")
            return []
    
    def _extract_reward(self, title: str, body: str) -> float:
        """Extract reward amount from title or body"""
        import re
        
        # Common patterns: $100, 100 USD, 100 RTC, etc.
        patterns = [
            r'\$(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*(?:USD|RTC|ETH|BTC|DAI)',
            r'bounty.*?\$?(\d+(?:\.\d+)?)',
            r'reward.*?\$?(\d+(?:\.\d+)?)',
        ]
        
        text = f"{title} {body}"
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    return float(matches[0])
                except ValueError:
                    continue
        
        return 0.0
    
    def track_bounty(self, bounty_id: int, notes: str = ""):
        """Add a bounty to tracked list"""
        tracked = self._load_tracked()
        
        # Check if already tracked
        if any(b['id'] == bounty_id for b in tracked):
            print(f"Bounty {bounty_id} is already being tracked.")
            return
        
        # Fetch full issue details
        # Note: This is simplified - would need owner/repo/number
        tracked.append({
            'id': bounty_id,
            'notes': notes,
            'status': 'tracking',
            'added_at': datetime.now().isoformat(),
            'claimed': False,
            'completed': False
        })
        
        self._save_tracked(tracked)
        
        stats = self._load_stats()
        stats['total_tracked'] += 1
        self._save_stats(stats)
        
        print(f"✅ Now tracking bounty {bounty_id}")
    
    def list_tracked(self, status: Optional[str] = None) -> List[Dict]:
        """List all tracked bounties"""
        tracked = self._load_tracked()
        
        if status:
            tracked = [b for b in tracked if b.get('status') == status]
        
        return tracked
    
    def update_status(self, bounty_id: int, status: str, notes: str = ""):
        """Update bounty status"""
        tracked = self._load_tracked()
        
        for bounty in tracked:
            if bounty['id'] == bounty_id:
                bounty['status'] = status
                if notes:
                    bounty['notes'] = notes
                bounty['updated_at'] = datetime.now().isoformat()
                
                if status == 'completed':
                    bounty['completed'] = True
                    stats = self._load_stats()
                    stats['completed'] += 1
                    self._save_stats(stats)
                
                self._save_tracked(tracked)
                print(f"✅ Updated bounty {bounty_id} to status: {status}")
                return
        
        print(f"❌ Bounty {bounty_id} not found in tracked list.")
    
    def get_stats(self) -> Dict:
        """Get hunting statistics"""
        return self._load_stats()
    
    def export_report(self, output_file: str = "bounty_report.md"):
        """Export a markdown report of tracked bounties"""
        tracked = self._load_tracked()
        stats = self._load_stats()
        
        with open(output_file, 'w') as f:
            f.write("# 🎯 Bounty Hunter Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            f.write("## 📊 Statistics\n\n")
            f.write(f"- Total Bounties Searched: {stats['total_searched']}\n")
            f.write(f"- Currently Tracking: {stats['total_tracked']}\n")
            f.write(f"- Completed: {stats['completed']}\n")
            f.write(f"- Total Earnings: ${stats['earnings']:.2f}\n\n")
            
            f.write("## 📋 Tracked Bounties\n\n")
            
            status_order = ['tracking', 'claimed', 'in_progress', 'completed', 'abandoned']
            by_status = {}
            for bounty in tracked:
                status = bounty.get('status', 'unknown')
                if status not in by_status:
                    by_status[status] = []
                by_status[status].append(bounty)
            
            for status in status_order:
                if status in by_status:
                    f.write(f"### {status.upper()}\n\n")
                    for bounty in by_status[status]:
                        f.write(f"- **ID**: {bounty['id']}\n")
                        f.write(f"  - Status: {bounty['status']}\n")
                        f.write(f"  - Added: {bounty.get('added_at', 'N/A')}\n")
                        if bounty.get('notes'):
                            f.write(f"  - Notes: {bounty['notes']}\n")
                        f.write("\n")
        
        print(f"✅ Report exported to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="🔍 GitHub Bounty Hunter - Find and track bounty opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search                    # Search for all bounties
  %(prog)s search -l python -m 50    # Python bounties with $50+ reward
  %(prog)s track 12345               # Track bounty #12345
  %(prog)s list                      # List tracked bounties
  %(prog)s stats                     # Show statistics
  %(prog)s report                    # Generate markdown report
        """
    )
    
    parser.add_argument('--token', '-t', help='GitHub API token (or set GITHUB_TOKEN env var)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for bounties')
    search_parser.add_argument('--query', '-q', default='bounty', help='Search query')
    search_parser.add_argument('--language', '-l', help='Filter by programming language')
    search_parser.add_argument('--min-reward', '-m', type=float, help='Minimum reward amount')
    search_parser.add_argument('--limit', '-n', type=int, default=30, help='Max results')
    
    # Track command
    track_parser = subparsers.add_parser('track', help='Track a bounty')
    track_parser.add_argument('id', type=int, help='Bounty ID')
    track_parser.add_argument('--notes', help='Add notes about this bounty')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tracked bounties')
    list_parser.add_argument('--status', '-s', help='Filter by status')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update bounty status')
    update_parser.add_argument('id', type=int, help='Bounty ID')
    update_parser.add_argument('status', choices=['tracking', 'claimed', 'in_progress', 'completed', 'abandoned'])
    update_parser.add_argument('--notes', help='Add/update notes')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('--output', '-o', default='bounty_report.md', help='Output file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    hunter = BountyHunter(token=args.token)
    
    if args.command == 'search':
        print(f"🔍 Searching for bounties...")
        bounties = hunter.search_bounties(
            query=args.query,
            language=args.language,
            min_reward=args.min_reward,
            max_results=args.limit
        )
        
        if not bounties:
            print("No bounties found.")
            return
        
        print(f"\nFound {len(bounties)} bounties:\n")
        print(f"{'ID':<12} {'Reward':<10} {'Repo':<25} {'Title':<40}")
        print("-" * 90)
        
        for b in bounties:
            reward = f"${b['estimated_reward']:.0f}" if b['estimated_reward'] > 0 else "?"
            repo = f"{b['owner']}/{b['repository']}"[:24]
            title = b['title'][:38]
            print(f"{b['id']:<12} {reward:<10} {repo:<25} {title:<40}")
        
        print(f"\n💡 Use `bounty-hunter track <ID>` to track a bounty")
    
    elif args.command == 'track':
        hunter.track_bounty(args.id, args.notes or "")
    
    elif args.command == 'list':
        tracked = hunter.list_tracked(args.status)
        if not tracked:
            print("No tracked bounties found.")
            return
        
        print(f"\n📋 Tracked Bounties ({len(tracked)} total):\n")
        print(f"{'ID':<12} {'Status':<15} {'Added':<20} {'Notes':<30}")
        print("-" * 80)
        
        for b in tracked:
            added = b.get('added_at', 'N/A')[:19]
            notes = (b.get('notes') or '')[:28]
            print(f"{b['id']:<12} {b['status']:<15} {added:<20} {notes:<30}")
    
    elif args.command == 'update':
        hunter.update_status(args.id, args.status, args.notes or "")
    
    elif args.command == 'stats':
        stats = hunter.get_stats()
        print("\n📊 Bounty Hunter Statistics\n")
        print(f"Total Searched:    {stats['total_searched']}")
        print(f"Currently Tracking: {stats['total_tracked']}")
        print(f"Completed:         {stats['completed']}")
        print(f"Total Earnings:    ${stats['earnings']:.2f}")
        print(f"First Run:         {stats['first_run'][:10]}")
    
    elif args.command == 'report':
        hunter.export_report(args.output)


if __name__ == '__main__':
    main()