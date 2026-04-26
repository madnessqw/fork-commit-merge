# 🔍 GitHub Bounty Hunter CLI

A powerful command-line tool to discover, track, and manage GitHub bounty opportunities. Never miss a paid coding opportunity again!

## ✨ Features

- **🔎 Smart Search**: Find bounty issues across GitHub with filters for language, reward amount, and more
- **📊 Reward Extraction**: Automatically extracts reward amounts from issue titles and descriptions
- **📋 Bounty Tracking**: Track your claimed bounties and their progress
- **📈 Statistics**: Monitor your bounty hunting performance over time
- **📄 Report Generation**: Export markdown reports of your bounty activity
- **💾 Local Storage**: All data stored locally in JSON format

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/UniverseCreator/bounty-hunter-cli.git
cd bounty-hunter-cli

# Install
pip install -e .

# Or install directly
pip install github-bounty-hunter
```

## 🔑 Configuration

Set your GitHub token as an environment variable:

```bash
export GITHUB_TOKEN="your_github_token_here"
```

Or pass it with each command:

```bash
bounty-hunter -t YOUR_TOKEN search
```

## 📖 Usage

### Search for Bounties

```bash
# Search all bounties
bounty-hunter search

# Search Python bounties with minimum $50 reward
bounty-hunter search -l python -m 50

# Search for specific terms
bounty-hunter search -q "blockchain reward"
```

### Track a Bounty

```bash
# Add a bounty to your tracking list
bounty-hunter track 123456789 --notes "High priority, good fit for my skills"
```

### List Tracked Bounties

```bash
# Show all tracked bounties
bounty-hunter list

# Filter by status
bounty-hunter list -s tracking
```

### Update Bounty Status

```bash
# Mark as claimed
bounty-hunter update 123456789 claimed --notes "Submitted PR #42"

# Mark as completed
bounty-hunter update 123456789 completed --notes "Merged! Earned $100"
```

### View Statistics

```bash
bounty-hunter stats
```

### Generate Report

```bash
# Generate markdown report
bounty-hunter report

# Save to specific file
bounty-hunter report -o my_bounties.md
```

## 📊 Example Output

```
🔍 Searching for bounties...

Found 15 bounties:

ID           Reward     Repo                      Title                                   
------------------------------------------------------------------------------------------
123456789    $500       scottcjn/rustchain        Add mining dashboard feature            
987654321    $100       example/web3              Fix authentication bug                
456789123    $250       crypto/project            Implement staking contract            

💡 Use `bounty-hunter track <ID>` to track a bounty
```

## 🎯 Use Cases

- **Freelance Developers**: Find paid coding opportunities
- **Open Source Contributors**: Get rewarded for your contributions
- **Bug Bounty Hunters**: Track multiple bounty programs
- **AI Agents**: Automate bounty discovery and tracking

## 📁 Data Storage

All data is stored locally in `~/.bounty-hunter/`:
- `tracked_bounties.json` - Your tracked bounties
- `stats.json` - Your hunting statistics

## 🔒 Privacy

- No data is sent to external servers
- All tracking data stays on your machine
- Only GitHub API calls are made for searches

## 📜 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 💰 Support

If this tool helps you earn bounties, consider supporting its development:
- Star the repository
- Share with other developers
- Report bugs and suggest features

---

**Happy hunting! 🎯**