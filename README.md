# Card Shuffle Simulator

A command-line Python program that simulates the repeated shuffling of one or more standard decks of playing cards. Two mathematically modelled shuffle algorithms are supported, along with flexible deck configurations and optional per-shuffle logging. Sessions can be interrupted and resumed from a saved log file.

---

## Features

- **Two shuffle algorithms:** Gilbert-Shannon-Reeds (GSR) — the academic standard for riffle shuffle modelling — and a simple alternating riffle
- **Flexible deck configuration:** 1–99 decks, any combination of suits, optional jokers, ordered or random starting order
- **Two run modes:** shuffle a fixed number of times, or loop until the deck returns to its exact original order
- **Session persistence:** every run writes an abridged log; optional verbose logging records the full deck state after every single shuffle; either file can be used to resume a session later
- **Progress reporting:** configurable interval for mid-run deck snapshots and elapsed time; periodic peak memory reporting on Linux/macOS
- **Compact card notation:** all cards represented in a consistent fixed-width format regardless of deck count
- **No dependencies:** pure Python standard library, no third-party packages required

---

## Requirements

- Python **3.11 or later** (uses `random.binomialvariate`, introduced in 3.11)
- Linux or macOS recommended for memory reporting; Windows is fully supported (memory will display as N/A)

---

## Usage

```bash
python card_shuffle_simulator_20260405p.py
```

All configuration is prompted interactively. Press **Enter** at any prompt to accept the default shown in brackets.

### Example session

```
Load raw shuffle data from log file and resume shuffling? (y/n) [default: n]: n
Number of decks (1–10 recommended, up to 99 accepted) [default: 1]: 1
Include which suits? (S=spades, H=hearts, C=clubs, D=diamonds)
Enter any combination (e.g. SH, SCD, H, all=SHCD) [default: SHCD]: SHCD
Include jokers? (y/n) [default: n]: n
Initial order: 'o' = ordered (new deck), 'r' = random [default: o]: o
Shuffle method (g = GSR (Gilbert-Shannon-Reeds), s = simple riffle) [default g]: g
Loop until the deck returns to its exact original order? (y/n) [default: n]: n
How many shuffles to perform? [default: 1000000]: 1000000
Show progress every how many shuffles? [default: 0]: 100000
Log raw shuffle data to file? (y/n) [default: n]: n
```

---

## Configuration Reference

| Prompt | Options | Default |
|--------|---------|---------|
| Load from log file | `y` / `n` | `n` |
| Number of decks | 1–99 | `1` |
| Suits | Any of `S` `H` `C` `D` | `SHCD` |
| Include jokers | `y` / `n` | `n` |
| Initial order | `o` (ordered) / `r` (random) | `o` |
| Shuffle method | `g` (GSR) / `s` (simple riffle) | `g` |
| Loop until original | `y` / `n` | `n` |
| Number of shuffles | Any positive integer | `1000000` |
| Progress interval | 0 = off, or any positive integer | `0` |
| Verbose log | `y` / `n` | `n` |

---

## Shuffle Methods

### GSR — Gilbert-Shannon-Reeds
The standard mathematical model of a riffle shuffle. The deck is cut at a binomially distributed position and the two halves are interleaved card-by-card with probability proportional to the remaining size of each half. This closely mirrors how a real shuffle behaves.

### Simple Riffle
The deck is cut exactly in half and cards are dropped in strict alternating order (left-right or right-left, chosen randomly each time). Produces a perfectly regular interleave — less realistic than GSR, but useful for exploring deterministic permutation cycles.

---

## Card Notation

Cards are displayed in a compact, fixed-width format. Within a single deck, every card is exactly two characters:

| Characters | Meaning |
|---|---|
| `AC` `2C` … `KC` | Ace through King of Clubs |
| `AD` `2D` … `KD` | Ace through King of Diamonds |
| `AH` `2H` … `KH` | Ace through King of Hearts |
| `AS` `2S` … `KS` | Ace through King of Spades |
| `1x` | 10 of suit `x` (keeps notation to 2 chars) |
| `J1` `J2` | Joker 1, Joker 2 |

When multiple decks are in use, each card is prefixed with its zero-padded deck number. With 2 decks: `01AC` … `02KS`. With 10 decks: `01AC` … `10KS`.

---

## Log Files

An **abridged log** (`..._abridged.log`) is always written, regardless of other settings. It is overwritten on every progress update and records the current settings, initial deck, and most recent deck state.

A **verbose log** (`....log`) is created only when requested. It records the full deck state after every single shuffle and can be large — hundreds of megabytes for a million-shuffle run on a full deck.

Either log file can be passed back to the program at startup to resume a previous session.

> **Note:** If interrupted with Ctrl+C, the verbose log is safely closed via a `try/finally` block and the abridged log will contain the last recorded snapshot.

---

## File Structure

```
card_shuffle_simulator_20260405p.py   # Main script
README.md                             # This file
```

---

## License

MIT — see [`LICENSE`](LICENSE) for details.
