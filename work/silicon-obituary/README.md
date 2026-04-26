# Silicon Obituary Generator

A Python tool that generates poetic memorials for retired RustChain miners.

## Bounty
- **Issue:** #2308
- **Reward:** 25 RTC
- **Repository:** Scottcjn/rustchain-bounties

## Features

### Core Functionality
- Detects when a miner hasn't attested in 7+ days
- Pulls miner data: first attestation, total epochs, RTC earned, architecture
- Generates poetic eulogies using multiple templates
- Creates BoTTube video scripts
- Outputs Discord notifications

### Eulogy Templates
4 unique poetic templates covering:
- Traditional obituary format
- Service record style
- Hashtag-optimized social format
- Narrative storytelling

### Supported Architectures
- PowerPC G3/G4/G5
- SPARC
- MIPS
- SGI
- DEC Alpha

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Generate a Single Obituary

```python
from silicon_obituary import generate_miner_data, generate_eulogy

# Create miner data
miner = generate_miner_data("dual-g4-125", "powerpc-g4")
miner["epochs"] = 847
miner["rtc"] = 412.5
miner["first_attestation"] = "2025-01-15"
miner["last_attestation"] = "2026-03-20"

# Generate eulogy
eulogy = generate_eulogy(miner)
print(eulogy)
```

### Generate BoTTube Video Script

```python
from silicon_obituary import generate_bottube_script

script = generate_bottube_script(eulogy, miner)
print(script)
```

### Batch Processing

```python
from silicon_obituary import process_retired_miners

# Process all miners inactive for 7+ days
retired_miners = [
    {"id": "dual-g4-125", "arch": "powerpc-g4", "last_attestation": "2026-03-10"},
    {"id": "sparc-ultra-42", "arch": "sparc", "last_attestation": "2026-03-08"},
]

for miner_info in retired_miners:
    miner_data = generate_miner_data(miner_info["id"], miner_info["arch"])
    eulogy = generate_eulogy(miner_data)
    script = generate_bottube_script(eulogy, miner_data)
    
    # Save to file
    with open(f"obituaries/{miner_info['id']}.md", "w") as f:
        f.write(eulogy)
```

## Example Output

```
Here lies dual-g4-125, a PowerPC G4.

It attested for 847 epochs and earned 412 RTC.
Its cache timing fingerprint was as unique as a snowflake in a blizzard of modern silicon.

Born in 1999, it faithfully served 1.2 years before joining the network.
It is survived by its power supply, which still hums with potential.

Not all heroes wear capes. Some wear heat sinks.
```

## Files

- `silicon_obituary.py` - Main generator module
- `example_output/` - Sample obituaries and scripts
- `tests/` - Unit tests

## Wallet

RTC wallet for bounty payout: (to be provided in PR)

## License

MIT - Created for RustChain Bounty #2308
