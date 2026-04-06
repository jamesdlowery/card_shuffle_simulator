# Card Shuffle Simulator — User Guide

**Version:** 20260405p  
**Language:** Python 3

---

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Starting the Program](#starting-the-program)
4. [Configuration Options](#configuration-options)
5. [Shuffle Methods](#shuffle-methods)
6. [Log Files](#log-files)
7. [Resuming a Session](#resuming-a-session)
8. [Card Notation](#card-notation)
9. [Tips and Notes](#tips-and-notes)

---

## Overview

The Card Shuffle Simulator is a command-line Python program that simulates the repeated shuffling of one or more standard decks of playing cards. It supports two mathematically modelled shuffle algorithms, flexible deck configurations (number of decks, suits, jokers), and optional logging of every shuffle to disk. Sessions can be paused and resumed later from a saved log file.

---

## Requirements

- Python 3.11 or later (required for `random.binomialvariate`)
- A Unix-like operating system (Linux or macOS) for memory reporting; Windows is supported but memory usage will display as N/A
- No third-party packages are required

---

## Starting the Program

Run the script from a terminal:

```
python card_shuffle_simulator_20260405p.py
```

The program will prompt you for all settings interactively. Press **Enter** at any prompt to accept the default value shown in brackets.

---

## Configuration Options

### Load from log file?

```
Load raw shuffle data from log file and resume shuffling? (y/n) [default: n]:
```

- Enter `y` to resume a previous session from a saved log file.
- Enter `n` (or press Enter) to start a fresh session.

---

### Number of decks

```
Number of decks (1–10 recommended, up to 99 accepted) [default: 1]:
```

Sets how many standard 52-card decks are combined into one shuffled pack. Values from 1 to 99 are accepted; 1–10 is the recommended range for practical use.

---

### Suits

```
Include which suits? (S=spades, H=hearts, C=clubs, D=diamonds)
Enter any combination (e.g. SH, SCD, H, all=SHCD) [default: SHCD]:
```

Choose which suits to include. Any combination of S, H, C, and D is valid. Enter them in any order. If you enter nothing or an invalid string, all four suits are used.

| Input | Result |
|-------|--------|
| `SHCD` | Full deck (default) |
| `SH` | Spades and Hearts only (26 cards per deck) |
| `D` | Diamonds only (13 cards per deck) |

---

### Jokers

```
Include jokers? (y/n) [default: n]:
```

If `y`, two jokers (J1 and J2) are added to each deck.

---

### Initial order

```
Initial order: 'o' = ordered (new deck), 'r' = random [default: o]:
```

- `o` — Start with an ordered deck (suits grouped, ranks Ace through King).
- `r` — Start with a randomly shuffled deck.

---

### Shuffle method

```
Shuffle method (g = GSR (Gilbert-Shannon-Reeds), s = simple riffle) [default g]:
```

See [Shuffle Methods](#shuffle-methods) below for a description of each.

---

### Loop until original order

```
Loop until the deck returns to its exact original order? (y/n) [default: n]:
```

- `y` — Shuffle indefinitely until the deck happens to return to its exact starting configuration. This can take an extremely large number of shuffles.
- `n` — Shuffle a fixed number of times (see below).

---

### Number of shuffles (fixed-count mode only)

```
How many shuffles to perform? [default: 1000000]:
```

Only shown when **Loop until original** is `n`. Enter any positive integer.

---

### Progress interval

```
Show progress every how many shuffles? [default: 0]:
```

- `0` — No intermediate progress output.
- Any positive integer N — Print the current deck state and elapsed time every N shuffles. Memory usage is also printed every 10×N shuffles.

---

### Verbose log file

```
Log raw shuffle data to file? (y/n) [default: n]:
```

If `y`, every shuffle result is written to a timestamped `.log` file. This file can be used to resume the session later. Note: verbose logs grow very large quickly (one line per shuffle).

---

## Shuffle Methods

### GSR — Gilbert-Shannon-Reeds (default)

A mathematically accurate model of a real riffle shuffle. The deck is cut into two halves using a binomial distribution (so the cut point varies naturally), and cards are interleaved one at a time with probability proportional to the remaining size of each half. This is the standard model used in academic research on card shuffling.

### Simple Riffle

A deterministic alternating interleave: the deck is cut exactly in half, and cards are dropped strictly alternating left-right (or right-left, chosen randomly). This produces a perfectly regular interleave every time and is less realistic than GSR, but useful for studying structured permutations.

---

## Log Files

The simulator always writes an **abridged log file**, regardless of whether verbose logging is enabled.

### Abridged log (`..._abridged.log`)

Updated at each progress interval and at the end of the run. Contains:

- All initial settings
- The initial deck order (as raw card IDs)
- The most recently seen deck state, with elapsed time

This file is overwritten on each update — it always reflects the latest known state.

### Verbose log (`....log`)

Only created when you answer `y` to "Log raw shuffle data to file?". Contains:

- All initial settings
- The initial deck order
- One line per shuffle: shuffle number, full deck state (raw IDs), and elapsed time

**Warning:** At one million shuffles with a single full deck, this file will be hundreds of megabytes.

---

## Resuming a Session

To resume from a previous run:

1. Run the program and answer `y` to the first prompt.
2. Enter the filename of either the verbose log or the abridged log.

**From the verbose log:** The program reads back all settings and the full shuffle history, resuming from the last recorded shuffle.

**From the abridged log:** The program reads back settings and the most recently saved deck state. Because only the last visible state is stored, the exact shuffle count may be an approximation.

If the session had already completed (the target shuffle count was reached, or the deck returned to its original order), the program will report this and exit without shuffling further.

---

## Card Notation

Cards are displayed in a compact two-character format (per card, within a single deck):

| Character(s) | Meaning |
|---|---|
| `A` | Ace |
| `2`–`9` | Numbered cards 2–9 |
| `1` | 10 |
| `J` | Jack |
| `Q` | Queen |
| `K` | King |
| `C` | Clubs |
| `D` | Diamonds |
| `H` | Hearts |
| `S` | Spades |
| `J1` / `J2` | Joker 1 / Joker 2 |

Examples: `AC` = Ace of Clubs, `1H` = 10 of Hearts, `KS` = King of Spades.

**Multiple decks:** When more than one deck is in use, each card is prefixed with its deck number, zero-padded to the number of digits needed. For example, with two decks: `01AC`, `02KS`. With ten decks: `01AC` through `10KS`.

---

## Tips and Notes

- **The "loop until original" mode can run for an astronomically long time.** For a GSR shuffle, the expected number of shuffles before a deck returns to its original order grows extremely rapidly with deck size. Enable progress reporting and verbose logging if you intend to let it run unattended.

- **Verbose logging slows things down significantly** for large numbers of shuffles. Disable it if raw speed is the priority.

- **The abridged log is always safe to resume from**, even if the verbose log was not enabled. It won't have the exact intermediate shuffle count, but it will have the correct deck state.

- **Keyboard interrupt (Ctrl+C):** If you interrupt the program, the verbose log file will still be properly closed (the program uses a `try/finally` block), and the last abridged log snapshot will be intact. You can resume from either file.

- **Windows users:** Memory reporting will show "N/A" — this is expected and does not affect functionality.
