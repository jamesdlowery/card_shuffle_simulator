import random
import datetime
import resource
import sys
import time
from datetime import timezone

def card_to_str(card_id, num_decks, deck_size):
    deck_num = (card_id // deck_size) + 1
    local_id = card_id % deck_size
    prefix = ''
    if num_decks > 1:
        digits = len(str(num_decks))
        prefix = f"{deck_num:0{digits}d}"
    if local_id < 52:
        suit_id = local_id // 13
        rank_id = local_id % 13
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '1', 'J', 'Q', 'K']
        suits = ['C', 'D', 'H', 'S']
        return prefix + ranks[rank_id] + suits[suit_id]
    else:
        if local_id == 52:
            return prefix + 'J1'
        else:
            return prefix + 'J2'

def build_deck(num_decks, include_jokers, initial_order):
    deck_size = 54 if include_jokers == 'y' else 52
    deck = []
    for d in range(num_decks):
        for c in range(deck_size):
            deck.append(d * deck_size + c)
    if initial_order == 'r':
        random.shuffle(deck)
    return deck

def gsr_shuffle(deck):
    n = len(deck)
    left_size = random.binomialvariate(n, 0.5)
    left = deck[:left_size]
    right = deck[left_size:]
    shuffled = []
    while left or right:
        if not left:
            shuffled.extend(right)
            break
        if not right:
            shuffled.extend(left)
            break
        p_left = len(left) / (len(left) + len(right))
        if random.random() < p_left:
            shuffled.append(left.pop(0))
        else:
            shuffled.append(right.pop(0))
    return shuffled

def simple_riffle(deck):
    n = len(deck)
    k = n // 2
    left = deck[:k]
    right = deck[k:]
    shuffled = []
    start_left = random.random() < 0.5
    i = 0
    j = 0
    while i < len(left) or j < len(right):
        if start_left:
            if i < len(left):
                shuffled.append(left[i])
                i += 1
            if j < len(right):
                shuffled.append(right[j])
                j += 1
        else:
            if j < len(right):
                shuffled.append(right[j])
                j += 1
            if i < len(left):
                shuffled.append(left[i])
                i += 1
    return shuffled

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = seconds // 60
        secs = seconds % 60
        return f"{int(mins)}m {int(secs)}s"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{int(hours)}h {int(mins)}m {int(secs)}s"

# Cache peak memory at startup
_peak_mem_mb = None

def get_resources():
    global _peak_mem_mb
    if _peak_mem_mb is None:
        mem_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = mem_kb / 1024
        if sys.platform == 'darwin':
            mem_mb /= 1024  # macOS reports bytes
        _peak_mem_mb = mem_mb
    return f"Peak memory: {_peak_mem_mb:.1f} MB"

def parse_elapsed_from_line(val):
    """Extract elapsed float from '1 2 3 ... elapsed: 45.67' or return 0"""
    parts = val.split()
    if not parts:
        return 0.0
    last = parts[-1]
    if last.startswith('elapsed:'):
        try:
            return float(last.split(':', 1)[1])
        except:
            pass
    return 0.0

def main():
    global _peak_mem_mb
    get_resources()  # force caching

    load_str = input("Load raw shuffle output from file? (y/n) [default: n]: ") or 'n'
    load = load_str.lower() == 'y'

    time_offset = 0.0
    log_file = None

    if load:
        filename = input("Enter the log file name: ")
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        params = {}
        original = None
        last_deck = None
        last_count = 0
        last_elapsed = 0.0

        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()

            if key == 'Initial':
                try:
                    original = [int(x) for x in val.split()]
                except ValueError:
                    print("Warning: Invalid 'Initial' line in log")
                    continue
            elif key.startswith('Shuffle '):
                num_str = key[8:].strip()
                if num_str.isdigit():
                    try:
                        count_candidate = int(num_str)
                        deck_part = val.split('elapsed:')[0].strip()
                        deck_candidate = [int(x) for x in deck_part.split() if x.isdigit()]
                        last_count = count_candidate
                        last_deck = deck_candidate
                        last_elapsed = parse_elapsed_from_line(val)
                    except ValueError:
                        print(f"Warning: Invalid shuffle data on line: {line}")
                        continue
            else:
                params[key] = val

        if original is None:
            print("Error: No valid 'Initial' state found in log file.")
            return

        time_offset = last_elapsed

        num_decks = int(params.get('Number of decks', 1))
        include_jokers = params.get('Include jokers', 'n').lower()
        deck_size = 54 if include_jokers == 'y' else 52
        loop_until = params.get('Loop until original', 'n').lower() == 'y'
        num_shuffles_param = int(params.get('How many shuffles', 1000000)) if not loop_until else 0
        method = params.get('Shuffle method', 'g').lower()
        progress_every = int(params.get('Show progress every how many shuffles', 0))

        deck = last_deck if last_deck else original[:]
        count = last_count

        completed = False
        if loop_until:
            if deck == original:
                completed = True
        else:
            if count >= num_shuffles_param:
                completed = True

        if completed:
            print("The script has already completed.")
            print(f"Final state after {count} shuffles (total time was ~{format_time(time_offset)}):")
            print(' '.join(card_to_str(c, num_decks, deck_size) for c in deck))
            return

        print("Beginning order: " + ' '.join(card_to_str(c, num_decks, deck_size) for c in original))
        if count > 0:
            print(f"Resuming from after {count} shuffles | Previous time: {format_time(time_offset)}")
            print(' '.join(card_to_str(c, num_decks, deck_size) for c in deck))
        else:
            print("No shuffles performed yet (log appears empty or invalid).")

        log_file = filename
        log = True

    else:
        num_decks_str = input("Number of decks (1–10 recommended) [default: 1]: ") or '1'
        num_decks = int(num_decks_str)
        jokers_str = input("Include jokers? (y/n) [default: n]: ") or 'n'
        include_jokers = jokers_str.lower()
        initial_order_str = input("Initial order: 'o' = ordered (new deck), 'r' = random [default: o]: ") or 'o'
        method_str = input("Shuffle method (g = GSR (Gilbert-Shannon-Reeds), s = simple riffle) [default g]: ") or 'g'
        method = method_str.lower()
        loop_str = input("Loop until the deck returns to its exact original order? (y/n) [default: n]: ") or 'n'
        loop_until = loop_str.lower() == 'y'
        progress_str = input("Show progress every how many shuffles? [default: 0]: ") or '0'
        progress_every = int(progress_str)
        num_shuffles_str = input("How many shuffles to perform? [default: 1000000]: ") or '1000000'
        num_shuffles_param = int(num_shuffles_str)
        log_str = input("Log raw shuffle output to file? (y/n) [default: n]: ") or 'n'
        log = log_str.lower() == 'y'

        deck_size = 54 if include_jokers == 'y' else 52
        original = build_deck(num_decks, include_jokers, initial_order_str.lower())
        deck = original[:]
        count = 0

        if log:
            timestamp = datetime.datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
            log_file = f"Card_Shuffle_Simulator_{timestamp}.log"
            with open(log_file, 'w') as f:
                f.write(f"Number of decks: {num_decks}\n")
                f.write(f"Include jokers: {include_jokers}\n")
                f.write(f"Initial order: {initial_order_str.lower()}\n")
                f.write(f"Shuffle method: {method}\n")
                f.write(f"Loop until original: {loop_str.lower()}\n")
                f.write(f"Show progress every how many shuffles: {progress_every}\n")
                f.write(f"How many shuffles: {num_shuffles_param}\n")
                f.write(f"Initial: {' '.join(map(str, original))}\n")

        print("Beginning order: " + ' '.join(card_to_str(c, num_decks, deck_size) for c in original))

    # Start timer after all inputs/setup
    session_start = time.time()

    # Perform shuffles
    shuffle_func = gsr_shuffle if method == 'g' else simple_riffle

    if loop_until:
        while True:
            deck = shuffle_func(deck)
            count += 1
            session_elapsed = time.time() - session_start
            total_elapsed = time_offset + session_elapsed

            if log and log_file:
                deck_str = ' '.join(map(str, deck))
                with open(log_file, 'a') as f:
                    f.write(f"Shuffle {count}: {deck_str} elapsed: {total_elapsed:.4f}\n")

            if deck == original:
                break

            if progress_every > 0 and count % progress_every == 0:
                res_str = get_resources() if count % (progress_every * 10) == 0 else ""
                sep = " | " if res_str else ""
                print(f"Shuffle {count} | Elapsed: {format_time(total_elapsed)}{sep}{res_str}")
                print(' '.join(card_to_str(c, num_decks, deck_size) for c in deck))
    else:
        target_shuffles = num_shuffles_param if not load else int(params.get('How many shuffles', 1000000))
        while count < target_shuffles:
            deck = shuffle_func(deck)
            count += 1
            session_elapsed = time.time() - session_start
            total_elapsed = time_offset + session_elapsed

            if log and log_file:
                deck_str = ' '.join(map(str, deck))
                with open(log_file, 'a') as f:
                    f.write(f"Shuffle {count}: {deck_str} elapsed: {total_elapsed:.4f}\n")

            if progress_every > 0 and count % progress_every == 0 and count != target_shuffles:
                res_str = get_resources() if count % (progress_every * 10) == 0 else ""
                sep = " | " if res_str else ""
                print(f"Shuffle {count} | Elapsed: {format_time(total_elapsed)}{sep}{res_str}")
                print(' '.join(card_to_str(c, num_decks, deck_size) for c in deck))

    total_elapsed = time_offset + (time.time() - session_start)
    print(f"After {count} shuffles | Total time: {format_time(total_elapsed)}")
    print(' '.join(card_to_str(c, num_decks, deck_size) for c in deck))

if __name__ == "__main__":
    main()
