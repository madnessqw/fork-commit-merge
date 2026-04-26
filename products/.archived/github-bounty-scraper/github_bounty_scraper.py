#!/usr/bin/env python3
"""
GitHub Bounty Scraper
Automatically find and filter paid open-source opportunities

Usage:
    python github_bounty_scraper.py --search "blockchain" --min-reward 10
    python github_bounty_scraper.py --export csv --output bounties.csv
"""

import argparse
import json
import csv
import re
from datetime import datetime
from typing import List, Dict, Optional


class BountyScraper:
    """Scrape and filter GitHub bounty opportunities"""
    
    def __init__(self):
        self.bounties = []
        
    def parse_reward(self, text: str) -> Optional[Dict]:
        """Extract reward amount and currency from issue text"""
        # Match patterns like "50 RTC", "$100", "10 USDT", "5 ETH"
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(RTC)',
            r'\$(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*(USDT|USD)',
            r'(\d+(?:\.\d+)?)\s*(ETH|BTC|SOL)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                currency = match.group(2).upper() if len(match.groups()) > 1 else 'USD'
                return {'amount': amount, 'currency': currency}
        return None
    
    def estimate_difficulty(self, text: str) -> str:
        """Estimate bounty difficulty based on keywords"""
        text_lower = text.lower()
        
        easy_keywords = ['documentation', 'readme', 'typo', 'badge', 'link', 'simple']
        medium_keywords = ['feature', 'dashboard', 'ui', 'test', 'bug fix']
        hard_keywords = ['smart contract', 'security', 'refactor', 'architecture']
        
        if any(kw in text_lower for kw in hard_keywords):
            return 'hard'
        elif any(kw in text_lower for kw in medium_keywords):
            return 'medium'
        else:
            return 'easy'
    
    def filter_bounties(self, 
                       min_reward: float = 0,
                       max_reward: float = float('inf'),
                       currencies: List[str] = None,
                       difficulty: str = None) -> List[Dict]:
        """Filter bounties by criteria"""
        filtered = []
        
        for bounty in self.bounties:
            reward = bounty.get('reward')
            if not reward:
                continue
                
            # Check reward range
            if reward['amount'] < min_reward or reward['amount'] > max_reward:
                continue
            
            # Check currency
            if currencies and reward['currency'] not in currencies:
                continue
            
            # Check difficulty
            if difficulty and bounty.get('difficulty') != difficulty:
                continue
            
            filtered.append(bounty)
        
        return sorted(filtered, 
                     key=lambda x: x['reward']['amount'], 
                     reverse=True)
    
    def export_csv(self, bounties: List[Dict], filename: str):
        """Export bounties to CSV"""
        if not bounties:
            print("No bounties to export")
            return
        
        fieldnames = ['title', 'url', 'reward_amount', 'reward_currency', 
                     'difficulty', 'created_at', 'repository']
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for bounty in bounties:
                writer.writerow({
                    'title': bounty.get('title', ''),
                    'url': bounty.get('url', ''),
                    'reward_amount': bounty['reward']['amount'],
                    'reward_currency': bounty['reward']['currency'],
                    'difficulty': bounty.get('difficulty', 'unknown'),
                    'created_at': bounty.get('created_at', ''),
                    'repository': bounty.get('repository', '')
                })
        
        print(f"Exported {len(bounties)} bounties to {filename}")
    
    def generate_report(self, bounties: List[Dict]) -> str:
        """Generate a text report of bounties"""
        if not bounties:
            return "No bounties found matching criteria"
        
        lines = [
            "=" * 60,
            "GITHUB BOUNTY REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 60,
            ""
        ]
        
        total_value = 0
        for bounty in bounties:
            reward = bounty['reward']
            lines.extend([
                f"Title: {bounty.get('title', 'N/A')}",
                f"Reward: {reward['amount']} {reward['currency']}",
                f"Difficulty: {bounty.get('difficulty', 'unknown')}",
                f"URL: {bounty.get('url', 'N/A')}",
                f"Repo: {bounty.get('repository', 'N/A')}",
                "-" * 40,
                ""
            ])
            total_value += reward['amount']
        
        lines.extend([
            "=" * 60,
            f"Total Bounties: {len(bounties)}",
            f"Total Value: ~{total_value:.2f} (mixed currencies)",
            "=" * 60
        ])
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Find and filter GitHub bounty opportunities'
    )
    parser.add_argument('--min-reward', type=float, default=0,
                       help='Minimum reward amount')
    parser.add_argument('--max-reward', type=float, default=float('inf'),
                       help='Maximum reward amount')
    parser.add_argument('--currency', nargs='+',
                       help='Filter by currency (RTC, USDT, ETH, etc.)')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'],
                       help='Filter by difficulty')
    parser.add_argument('--export', choices=['json', 'csv'],
                       help='Export format')
    parser.add_argument('--output', default='bounties',
                       help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    scraper = BountyScraper()
    
    # Example data (in real usage, this would come from GitHub API)
    example_bounties = [
        {
            'title': 'Add miner setup wizard',
            'url': 'https://github.com/example/repo/issues/1',
            'reward': {'amount': 50, 'currency': 'RTC'},
            'difficulty': 'medium',
            'created_at': '2026-03-20',
            'repository': 'example/repo'
        },
        {
            'title': 'Fix documentation typo',
            'url': 'https://github.com/example/repo/issues/2',
            'reward': {'amount': 5, 'currency': 'RTC'},
            'difficulty': 'easy',
            'created_at': '2026-03-21',
            'repository': 'example/repo'
        },
        {
            'title': 'Build dashboard UI',
            'url': 'https://github.com/example/repo/issues/3',
            'reward': {'amount': 100, 'currency': 'USDT'},
            'difficulty': 'hard',
            'created_at': '2026-03-22',
            'repository': 'example/repo'
        }
    ]
    
    scraper.bounties = example_bounties
    
    # Filter bounties
    filtered = scraper.filter_bounties(
        min_reward=args.min_reward,
        max_reward=args.max_reward,
        currencies=args.currency,
        difficulty=args.difficulty
    )
    
    # Output results
    if args.export == 'csv':
        scraper.export_csv(filtered, f"{args.output}.csv")
    elif args.export == 'json':
        with open(f"{args.output}.json", 'w') as f:
            json.dump(filtered, f, indent=2)
        print(f"Exported {len(filtered)} bounties to {args.output}.json")
    else:
        print(scraper.generate_report(filtered))


if __name__ == '__main__':
    main()
