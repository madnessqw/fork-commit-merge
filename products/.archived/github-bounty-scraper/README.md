# GitHub Bounty Scraper

Automatically find, filter, and track paid open-source opportunities on GitHub.

## Features

- 🔍 **Smart Reward Detection** - Automatically extracts bounty amounts from issue text
- 🎯 **Advanced Filtering** - Filter by reward amount, currency, and difficulty
- 📊 **Multiple Export Formats** - CSV, JSON, or formatted text reports
- 🏷️ **Difficulty Estimation** - Auto-categorizes bounties as easy/medium/hard
- 💰 **Value Tracking** - Calculate total potential earnings

## Installation

```bash
# Clone or download
cd github-bounty-scraper

# No dependencies required - uses only Python standard library
python3 --version  # Requires Python 3.6+
```

## Usage

### Basic Usage

```bash
# Show all bounties
python github_bounty_scraper.py

# Filter by minimum reward
python github_bounty_scraper.py --min-reward 25

# Filter by currency
python github_bounty_scraper.py --currency RTC USDT

# Filter by difficulty
python github_bounty_scraper.py --difficulty easy
```

### Export Results

```bash
# Export to CSV
python github_bounty_scraper.py --export csv --output my_bounties

# Export to JSON
python github_bounty_scraper.py --export json --output bounties
```

### Combined Filters

```bash
# Find easy bounties between $10-50 in RTC or USDT
python github_bounty_scraper.py \
  --min-reward 10 \
  --max-reward 50 \
  --currency RTC USDT \
  --difficulty easy \
  --export csv \
  --output easy_money
```

## Supported Currencies

The scraper automatically detects:
- **RTC** - RustChain Token
- **USDT** - Tether
- **ETH** - Ethereum
- **BTC** - Bitcoin
- **SOL** - Solana
- **USD** - US Dollars

## Difficulty Levels

Automatically estimated based on keywords:

| Level | Keywords | Typical Time |
|-------|----------|--------------|
| Easy | documentation, readme, typo, badge | 15-60 min |
| Medium | feature, dashboard, ui, test, bug fix | 2-6 hours |
| Hard | smart contract, security, refactor, architecture | 8+ hours |

## Example Output

```
============================================================
GITHUB BOUNTY REPORT
Generated: 2026-03-23 10:15
============================================================

Title: Build dashboard UI
Reward: 100 USDT
Difficulty: hard
URL: https://github.com/example/repo/issues/3
Repo: example/repo
----------------------------------------

Title: Add miner setup wizard
Reward: 50 RTC
Difficulty: medium
URL: https://github.com/example/repo/issues/1
Repo: example/repo
----------------------------------------

============================================================
Total Bounties: 2
Total Value: ~150.00 (mixed currencies)
============================================================
```

## Integration with GitHub API

To use with real GitHub data, modify the `main()` function to call the GitHub API:

```python
import requests

def fetch_github_bounties(self, query="label:bounty state:open"):
    """Fetch bounties from GitHub API"""
    url = f"https://api.github.com/search/issues"
    params = {
        'q': query,
        'sort': 'updated',
        'order': 'desc'
    }
    response = requests.get(url, params=params)
    # Parse and return bounty data
```

## Use Cases

1. **Daily Bounty Hunting** - Run daily to find new opportunities
2. **Portfolio Planning** - Identify bounties matching your skills
3. **Income Tracking** - Export and track potential earnings
4. **Market Research** - Analyze bounty trends and rates

## Tips for Success

1. **Start with easy bounties** - Build confidence and reputation
2. **Focus on one currency** - Reduces complexity
3. **Track your applications** - Use the CSV export for tracking
4. **Check issue age** - Older issues may be stale

## License

MIT License - Use freely for personal or commercial projects.

---

**Ready to start earning?** Run the scraper and find your first bounty today!
