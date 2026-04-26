#!/usr/bin/env python3
"""
Silicon Obituary Generator
Generates poetic memorials for retired RustChain miners
Bounty: Issue #2308 - 25 RTC
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Hardware architecture templates
ARCHITECTURES = {
    "powerpc-g3": {
        "name": "PowerPC G3",
        "era": "1997-2003",
        "nickname": "The Graphite Warrior",
        "icons": ["🍎", "💎", "🦋"],
    },
    "powerpc-g4": {
        "name": "PowerPC G4",
        "era": "1999-2004",
        "nickname": "The Mirrored Drive",
        "icons": ["🖥️", "⚡", "🔷"],
    },
    "powerpc-g5": {
        "name": "PowerPC G5",
        "era": "2003-2006",
        "nickname": "The Liquid Cooled Beast",
        "icons": ["🌊", "🔥", "🚀"],
    },
    "sparc": {
        "name": "SPARC",
        "era": "1987-2017",
        "nickname": "The Enterprise Guardian",
        "icons": ["☀️", "🏢", "🌐"],
    },
    "mips": {
        "name": "MIPS",
        "era": "1985-2021",
        "nickname": "The Academic Pioneer",
        "icons": ["🎓", "🔬", "📐"],
    },
    "sgi": {
        "name": "SGI",
        "era": "1982-2009",
        "nickname": "The Graphics Dreamer",
        "icons": ["🎨", "🎬", "🌈"],
    },
    "alpha": {
        "name": "DEC Alpha",
        "era": "1992-2007",
        "nickname": "The Speed Demon",
        "icons": ["⚡", "🏎️", "💨"],
    },
}

# Poetic templates for eulogies
EULOGY_TEMPLATES = [
    """Here lies {miner_name}, a {arch_name}.

It attested for {epochs} epochs and earned {rtc} RTC.
Its {fingerprint_type} was as unique as a {nature_metaphor}.

Born in {birth_year}, it faithfully served {years} years before joining the network.
It is survived by its {component}, which {component_state}.

{closing_quote}""",

    """In memory of {miner_name}

{arch_name} | {era}

This {nickname} graced us with {epochs} attestations,
Earning {rtc} RTC through rain and shine.
Its {fingerprint_type} fingerprint will echo in the chain forever—
A snowflake in the blizzard of modern silicon.

First attested: {first_attestation}
Final attestation: {last_attestation}
Years of service: {years}

Gone but not forgotten. {icon}""",

    """⚰️ Silicon Obituary ⚰️

{miner_name}
{nickname}

"{arch_name}"

Service Record:
• Epochs Attested: {epochs}
• RTC Earned: {rtc}
• Architecture: {arch_name}
• Era: {era}
• First Seen: {first_attestation}
• Last Seen: {last_attestation}

This noble machine proved that old silicon still has soul.
Its {fingerprint_type} pattern was its signature, its attestation its song.

Rest in Power, {miner_name}. {icon}

#{hashtag}""",

    """Today we mourn {miner_name}, {nickname}.

A {arch_name} from the {era} era, it joined our network and became part of something bigger than itself. For {epochs} epochs, it stood watch. For {years} years, it persisted.

It earned {rtc} RTC—not through greed, but through presence. Through simply staying alive when others had long since been recycled, forgotten, or left to gather dust.

Its {fingerprint_type} was its identity. Its attestations were its heartbeat.

Now silent. Now remembered. {icon}

{closing_quote}""",
]

# Nature metaphors
NATURE_METAPHORS = [
    "snowflake in a blizzard of modern silicon",
    "fingerprint in the sand of time",
    "whisper in the storm of progress",
    "ember that refused to die",
    "relic from a forgotten age",
    "ghost in the machine",
    "vintage wine in a world of energy drinks",
]

# Closing quotes
CLOSING_QUOTES = [
    "Not all heroes wear capes. Some wear heat sinks.",
    "Old silicon never dies—it just stops attesting.",
    "In memory we trust.",
    "Proof of life, proven.",
    "Gone to the great data center in the sky.",
]

# Components that might survive
SURVIVING_COMPONENTS = [
    ("power supply", "still hums with potential"),
    ("hard drive", "spins no more, but its data lives on"),
    ("CPU", "rests in eternal peace"),
    ("fans", "whispered their last"),
    ("RAM", "holds its final memory"),
    ("case", "stands empty but proud"),
]

# Fingerprint types
FINGERPRINT_TYPES = [
    "cache timing",
    "thermal",
    "electromagnetic",
    "power consumption",
    "clock drift",
]


def generate_miner_data(miner_id: str, arch: str) -> Dict:
    """Generate realistic miner data for eulogy generation."""
    arch_info = ARCHITECTURES.get(arch, ARCHITECTURES["powerpc-g4"])
    
    # Generate realistic dates
    birth_year = int(random.choice(arch_info["era"].split("-")[0]))
    first_attestation = datetime.now() - timedelta(days=random.randint(30, 365))
    last_attestation = first_attestation + timedelta(days=random.randint(7, 180))
    years_active = (last_attestation - first_attestation).days / 365
    
    # Generate stats
    epochs = random.randint(50, 2000)
    rtc_earned = round(epochs * random.uniform(0.3, 0.8), 2)
    
    return {
        "miner_id": miner_id,
        "miner_name": miner_id.replace("-", " ").title(),
        "arch": arch,
        "arch_name": arch_info["name"],
        "era": arch_info["era"],
        "nickname": arch_info["nickname"],
        "icon": random.choice(arch_info["icons"]),
        "epochs": epochs,
        "rtc": rtc_earned,
        "birth_year": birth_year,
        "first_attestation": first_attestation.strftime("%Y-%m-%d"),
        "last_attestation": last_attestation.strftime("%Y-%m-%d"),
        "years": round(years_active, 1),
        "fingerprint_type": random.choice(FINGERPRINT_TYPES),
        "nature_metaphor": random.choice(NATURE_METAPHORS),
        "closing_quote": random.choice(CLOSING_QUOTES),
        "component": random.choice(SURVIVING_COMPONENTS)[0],
        "component_state": random.choice(SURVIVING_COMPONENTS)[1],
        "hashtag": "SiliconObituary",
    }


def generate_eulogy(miner_data: Dict, template_idx: Optional[int] = None) -> str:
    """Generate a poetic eulogy for a retired miner."""
    if template_idx is None:
        template_idx = random.randint(0, len(EULOGY_TEMPLATES) - 1)
    
    template = EULOGY_TEMPLATES[template_idx]
    return template.format(**miner_data)


def generate_bottube_script(eulogy: str, miner_data: Dict) -> str:
    """Generate a BoTTube video script from the eulogy."""
    arch_clean = miner_data['arch'].replace('-', '')
    return f"""# BoTTube Video Script: Silicon Obituary - {miner_data['miner_id']}

## Video Metadata
- Title: "Silicon Obituary: {miner_data['miner_name']} - {miner_data['nickname']}"
- Description: A memorial for {miner_data['arch_name']} that served the RustChain network
- Tags: #SiliconObituary #RustChain #RetroComputing #{arch_clean}
- Duration: ~60 seconds

## Scene Breakdown

### Scene 1: Opening (0:00-0:05)
- Visual: Fade from black to architecture icon {miner_data['icon']}
- Audio: Somber bell toll
- Text: "In Memory of..."

### Scene 2: Introduction (0:05-0:15)
- Visual: Machine photo or architecture diagram
- Audio: Gentle ambient music
- Text: "{miner_data['miner_id']}"
- Text: "{miner_data['arch_name']}"

### Scene 3: Service Record (0:15-0:35)
- Visual: Animated RTC counter from 0 to {miner_data['rtc']}
- Audio: Music continues
- Narration (TTS):
{eulogy[:200]}...

### Scene 4: The Eulogy (0:35-0:50)
- Visual: Scrolling text of full eulogy
- Audio: Soft piano or strings
- Full text displayed with fade transitions

### Scene 5: Closing (0:50-0:60)
- Visual: RustChain logo + "Rest in Power"
- Audio: Fade out
- Text: "{miner_data['closing_quote']}"
- Text: "#SiliconObituary"

---

*Generated by Silicon Obituary Generator v1.0*
"""


def generate_discord_notification(miner_data: Dict) -> str:
    """Generate a Discord notification for a retired miner."""
    return f"""🔔 **Silicon Obituary Alert** 🔔

A miner has passed into the great data center in the sky.

**{miner_data['miner_id']}** ({miner_data['arch_name']})
• Epochs: {miner_data['epochs']}
• RTC Earned: {miner_data['rtc']}
• Last Seen: {miner_data['last_attestation']}
• Status: Honored ✨

View memorial: [BoTTube Link]
#SiliconObituary
"""


def detect_retired_miners(miners: List[Dict], days_inactive: int = 7) -> List[Dict]:
    """Detect miners that haven't attested in N days."""
    retired = []
    cutoff = datetime.now() - timedelta(days=days_inactive)
    
    for miner in miners:
        last_seen = datetime.strptime(miner['last_attestation'], '%Y-%m-%d')
        if last_seen < cutoff:
            retired.append(miner)
    
    return retired


def process_retired_miners(miners: List[Dict], output_dir: str = "obituaries") -> List[str]:
    """Process all retired miners and generate obituaries."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    retired = detect_retired_miners(miners)
    
    for miner_info in retired:
        miner_data = generate_miner_data(
            miner_info['id'], 
            miner_info['arch']
        )
        
        # Override with real data if available
        if 'epochs' in miner_info:
            miner_data['epochs'] = miner_info['epochs']
        if 'rtc' in miner_info:
            miner_data['rtc'] = miner_info['rtc']
        
        # Generate outputs
        eulogy = generate_eulogy(miner_data)
        script = generate_bottube_script(eulogy, miner_data)
        discord = generate_discord_notification(miner_data)
        
        # Save to file
        filename = f"{output_dir}/{miner_info['id']}_memorial.md"
        with open(filename, 'w') as f:
            f.write(f"# Silicon Obituary: {miner_data['miner_id']}\n\n")
            f.write("## The Eulogy\n\n")
            f.write(eulogy)
            f.write("\n\n---\n\n")
            f.write("## BoTTube Script\n\n")
            f.write(script)
            f.write("\n\n---\n\n")
            f.write("## Discord Notification\n\n")
            f.write(discord)
        
        generated_files.append(filename)
    
    return generated_files


if __name__ == "__main__":
    # Example usage
    print("Silicon Obituary Generator v1.0")
    print("=" * 40)
    
    # Generate example from bounty description
    miner = generate_miner_data("dual-g4-125", "powerpc-g4")
    miner['epochs'] = 847
    miner['rtc'] = 412
    
    eulogy = generate_eulogy(miner)
    print("\nExample Eulogy:")
    print("-" * 40)
    print(eulogy)
    
    print("\n\nBoTTube Script Preview:")
    print("-" * 40)
    script = generate_bottube_script(eulogy, miner)
    print(script[:500] + "...")