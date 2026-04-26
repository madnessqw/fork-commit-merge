# Polymarket Weather Apr 20 Shortlist — 2026-04-19

## Raw scan status
- Weather leaderboard page 1 + 2 public profiles scanned: 40
- Profiles with Apr 20 weather exposure: 8
- Distinct Apr 20 events seen: 23
- Important rule: profile title alone is not enough; outcome (Yes/No) must be read explicitly.

## Cleanest observed clusters
### 1) Seattle 62F or higher
- ColdMath: YES
- dpnd: YES
- 738925: NO (tiny)
- Market state checked on Polymarket: ~99.4% / Buy Yes ~99.7c
- Open-Meteo city forecast pulled in-session: ~22.2C / ~72.0F max
- Read: consensus is basically YES; probably not worth trading unless there is execution distortion.

### 2) Denver 40F or higher
- ColdMath: YES
- dpnd: YES
- 738925: NO (tiny)
- Market state checked on Polymarket: ~99.4% / Buy Yes ~99.5c
- Open-Meteo city forecast pulled in-session: ~25.8C / ~78.4F max
- Read: same story as Seattle; obvious direction, tiny edge at best.

### 3) Los Angeles ladder
- VibeTrader: YES 68-69F
- VibeTrader: YES 70-71F
- VibeTrader: YES 72-73F
- Market page checked on Polymarket: top bins ~68-69F 32%, 70-71F 25%, 66-67F 25%, 72-73F 5%, 74F+ 7%
- Open-Meteo city forecast pulled in-session: ~23.3C / ~73.9F max
- Read: this is not a simple yes/no thesis; it is a distribution expression. Interesting but messy.

### 4) London exact-bin disagreement
- RamsBR: YES 15C
- Market page checked on Polymarket: 14C 39%, 13C 32%, 15C 20%
- Open-Meteo city forecast pulled in-session: ~13.0C max
- Read: leaderboard trader is not aligned with the top market bin. Needs station-specific verification before any trade.

### 5) Atlanta tail-bin NO
- ColdMath: NO 69F or below
- Market page checked on Polymarket: 76-77F 39%, 74-75F 28%, 72-73F 13%, 69F or below ~1%
- Open-Meteo city forecast pulled in-session: ~23.8C / ~74.8F max
- Read: this is an outcome-aware example of why `outcome` matters. Trader is effectively betting against the cold-tail bin, not for it.

## Mixed / secondary clusters
- Miami:
  - gghff: YES 82-83F, NO 84-85F
  - RamsBR: YES 82-83F
- Tokyo:
  - fred5k: YES 21C, YES 22C
  - gghff: YES 23C
- Seoul:
  - VibeTrader: YES 15C
  - fred5k: YES 16C
- Wellington:
  - hkooooo: YES 15C
  - fred5k: YES 14C

## Pre-trade takeaway
- Obvious near-certainty markets exist, but they are mostly bad from an edge standpoint.
- The interesting stuff is in exact-bin or adjacent-bin markets, but those need station-specific forecast verification, not generic city weather.
- Best immediate candidates for deeper station-level check before trading:
  1. London Apr 20 (13C / 14C / 15C cluster)
  2. Los Angeles Apr 20 (66-67 / 68-69 / 70-71 / 72-73 ladder)
  3. Miami Apr 20 (82-83 vs 84-85)
  4. Seoul Apr 20 (15C vs 16C)

## File links
- Raw active-position dump: /home/gokhan/UniverseCreator/memory/polymarket-weather-apr20-active-2026-04-19.md
- Pattern notes: /home/gokhan/UniverseCreator/memory/polymarket-leaderboard-weather-2026-04-19.md
