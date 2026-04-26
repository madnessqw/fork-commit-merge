# Polymarket Leaderboard Weather Notes — 2026-04-19

## Core pattern
- Weather leaderboard'daki güçlü hesaplar çoğunlukla tek outcome kovalamıyor.
- En yaygın pattern: aynı event içinde 2-6 komşu bin / ladder açmak.
- Bu yapı tek tahminden çok dağılım satın almak gibi çalışıyor.
- Overall leaderboard ise çoğunlukla sports/crypto/event stack; weather trade kopyalamak için doğrudan uygun değil.

## Clean examples
### Two-leg adjacent split examples
- amj007 / London Apr 19
  - 14C: ~70%
  - 13C: ~30%
- amj007 / Istanbul Apr 19
  - 16C: ~61%
  - 15C: ~39%
- moonape1226 / Chicago Apr 18
  - 66-67F: ~87%
  - 62-63F: ~13%
- Poligarch / Atlanta Apr 18
  - 86-87F: ~51%
  - 84-85F: ~49%
- swisstony / sports example
  - Chelsea win: ~86%
  - Draw: ~14%

## Interpreting the pattern
- 87/13 gibi oranlar genelde ana tez + küçük tail hedge gibi okunmalı.
- 51/49 gibi oranlar ise tek noktaya inanç değil, yakın iki outcome arasında belirsizlik dağıtımı.
- 4-6 bacaklı ladder yapılar çoğu zaman market making / distribution expression; kör copy-trade için kötü.
- 2 bacaklı komşu split yapılar daha okunabilir ve analiz edilebilir.

## Sampled public profiles worth re-checking
- VibeTrader
- amj007
- moonape1226
- dpnd
- Poligarch
- swisstony

## Tactical takeaway
- Leaderboard = context
- Trade trigger = değil
- Trade öncesi mutlaka live market microstructure + hava verisi + expiry timing ile yeniden doğrula.
