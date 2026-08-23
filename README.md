# Card Shuffle Simulator

**Version:** 1.2.0  
**Date:** 2026-08-22  
**Language:** Python 3.8+

A high-fidelity text-based simulator of real-world card shuffling. It implements the mathematically rigorous Gilbert-Shannon-Reeds (GSR) model as well as a simpler alternating riffle, supports multi-deck configurations, selectable suits, optional jokers, long-running simulations, resume-from-log, dual logging, and progress reporting with resource monitoring.

## Features

- **Shuffle models**
  - Gilbert-Shannon-Reeds (GSR) – probabilistic binomial cut + weighted interleaving
  - Simple riffle – fixed cut + alternating merge with random starting side
- **Deck configuration**
  - 1–99 decks
  - Any combination of suits (S/H/C/D) – decks as small as 13 cards supported
  - Optional jokers (J1 / J2)
  - Ordered (new-deck) or random initial order
- **Execution modes**
  - Fixed number of shuffles
  - Loop until the deck returns to its exact original order (always alerts on return)
- **Logging & resume**
  - Always creates an abridged summary log (`*_abridged.log`)
  - Optional full verbose log of every shuffle (raw integer IDs + elapsed time)
  - Resume from either log type; elapsed time is cumulative across sessions
  - When resuming from a full verbose log, new results are appended
- **Progress & diagnostics**
  - Configurable progress interval
  - Elapsed wall-clock time (human-readable)
  - Peak memory reporting (cross-platform)
- **Performance**
  - Integer card IDs (no string manipulation in the hot loop)
  - O(n) GSR implementation using `collections.deque`
  - Verbose log file opened once and kept open for the entire run

## Requirements

- Python 3.8 or later
- Standard library only (`random`, `datetime`, `resource`, `sys`, `time`, `os`, `re`, `collections`)

On Windows the `resource` module is unavailable; peak-memory reporting gracefully degrades to “N/A”.

## Quick Start

```bash
python3 card_shuffle_simulator.py
```

Follow the interactive prompts. Defaults are shown in brackets.

Example minimal session (single deck, no jokers, GSR, 1 000 000 shuffles):

```
Load raw shuffle data from log file and resume shuffling? (y/n) [default: n]: 
Number of decks (1–10 recommended, up to 99 accepted) [default: 1]: 
Include which suits? ... [default: SHCD]: 
Include jokers? (y/n) [default: n]: 
Initial order: 'o' = ordered (new deck), 'r' = random [default: o]: 
Shuffle method (g = GSR ..., s = simple riffle) [default g]: 
Loop until the deck returns to its exact original order? (y/n) [default: n]: 
How many shuffles to perform? [default: 1000000]: 
Show progress every how many shuffles? [default: 0]: 
Log raw shuffle data to file? (y/n) [default: n]: 
```

## Log Files

| Type | Filename pattern | Content |
|------|------------------|---------|
| Abridged (always) | `card_shuffle_simulator_YYYYMMDDHHMMSS_abridged.log` | Settings, initial order, latest visible state + elapsed time |
| Verbose (optional) | `card_shuffle_simulator_YYYYMMDDHHMMSS.log` | Header + one line per shuffle (`Shuffle N: … elapsed: …`) |

Both formats can be loaded to resume a run. Editing the “How many shuffles” value in an abridged log allows continuing past the original target.

## Card Representation

- Internal: compact integer IDs
- Display: `AS`, `1H`, `KC`, … and `J1`/`J2` for jokers
- Multi-deck: numeric prefix without hyphen (`2AS`, `10KC`, …)
- Ten of a suit is abbreviated `1` (e.g. `1S` = ten of spades)

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.2.0 | 2026-08-22 | Resume from full verbose log now correctly appends; version string & docs added; cards_per_suit_set guaranteed in all paths |
| 1.1.x | 2026-04 | Iterative robustness, input validation, performance (deque), abridged logging, suits selection |
| 1.0 | earlier | Initial interactive simulator |

## License

Public domain / unrestricted use. No warranty.

## Author Notes

Developed iteratively with extensive attention to correctness (especially reduced-suit + joker edge cases), performance for multi-million-shuffle runs, and reliable resume semantics.
