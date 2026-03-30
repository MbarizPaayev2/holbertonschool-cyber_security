#!/usr/bin/python3
"""
read_write_heap.py - Finds a string in the heap of a running process and replaces it.

Usage: read_write_heap.py <pid> <search_string> <replace_string>
All strings are treated as ASCII.
"""

import sys


def usage_error(message):
    """Print error to stdout and exit with status 1"""
    print(f"Error: {message}")
    print("Usage: read_write_heap.py pid search_string replace_string")
    print("       pid must be an integer")
    print("       search_string and replace_string must be ASCII")
    sys.exit(1)


def get_heap_regions(pid):
    """
    Return list of (start, end) tuples for heap memory regions.
    Looks for [heap] first, then falls back to rw-p anonymous regions.
    """
    regions = []
    try:
        with open(f'/proc/{pid}/maps', 'r') as f:
            for line in f:
                if 'rw' not in line:
                    continue

                parts = line.split()
                addr_range = parts[0]
                pathname = parts[-1] if len(parts) > 5 else ""

                # Primary: [heap] label
                if '[heap]' in line:
                    try:
                        start, end = addr_range.split('-')
                        regions.append((int(start, 16), int(end, 16)))
                    except ValueError:
                        continue

                # Fallback: anonymous rw-p regions (common in some systems)
                elif not pathname.startswith('/') and 'rw-p' in line:
                    try:
                        start, end = addr_range.split('-')
                        regions.append((int(start, 16), int(end, 16)))
                    except ValueError:
                        continue

        if not regions:
            print("Warning: No [heap] found, trying anonymous rw regions...", file=sys.stdout)

        return regions

    except FileNotFoundError:
        usage_error(f"Process with PID {pid} not found.")
    except PermissionError:
        usage_error(f"Permission denied reading /proc/{pid}/maps. Try with sudo.")
    except Exception as e:
        usage_error(f"Failed to read memory maps: {e}")


def main():
    if len(sys.argv) != 4:
        usage_error("Incorrect number of arguments.")

    try:
        pid = int(sys.argv[1])
    except ValueError:
        usage_error("PID must be a valid integer.")

    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    if not search_str or not replace_str:
        usage_error("Search and replace strings cannot be empty.")

    try:
        search_bytes = search_str.encode('ascii')
        replace_bytes = replace_str.encode('ascii')
    except UnicodeEncodeError:
        usage_error("Strings must contain only ASCII characters.")

    # Get all heap regions
    heap_regions = get_heap_regions(pid)

    if not heap_regions:
        usage_error("No heap region found for this process.")

    replacements = 0
    changed_addrs = []

    try:
        with open(f'/proc/{pid}/mem', 'rb+') as mem:
            for start, end in heap_regions:
                size = end - start
                if size <= len(search_bytes):
                    continue

                print(f"Scanning heap: 0x{start:x} - 0x{end:x} ({size:,} bytes)", file=sys.stdout)

                mem.seek(start)
                try:
                    data = mem.read(size)
                except Exception:
                    print(f"  Could not read region 0x{start:x}", file=sys.stdout)
                    continue

                # Find all occurrences (non-overlapping)
                pos = 0
                while True:
                    pos = data.find(search_bytes, pos)
                    if pos == -1:
                        break

                    addr = start + pos

                    # Prepare replacement (same length, pad with \0 if shorter)
                    to_write = replace_bytes[:len(search_bytes)]
                    if len(to_write) < len(search_bytes):
                        to_write += b'\x00' * (len(search_bytes) - len(to_write))

                    # Write to memory
                    mem.seek(addr)
                    mem.write(to_write)

                    replacements += 1
                    changed_addrs.append(addr)

                    print(f"  Replaced at 0x{addr:x}: '{search_str}' → '{replace_str}'", file=sys.stdout)

                    pos += len(search_bytes)   # non-overlapping

    except PermissionError:
        usage_error(f"Permission denied accessing /proc/{pid}/mem. Run the script with sudo.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    # Final output
    print("\n=== Operation completed ===", file=sys.stdout)
    print(f"PID               : {pid}", file=sys.stdout)
    print(f"Search string     : '{search_str}'", file=sys.stdout)
    print(f"Replace string    : '{replace_str}'", file=sys.stdout)
    print(f"Heap regions      : {len(heap_regions)}", file=sys.stdout)
    print(f"Replacements made : {replacements}", file=sys.stdout)

    if changed_addrs:
        print("Modified addresses:", file=sys.stdout)
        for a in changed_addrs:
            print(f"  0x{a:x}", file=sys.stdout)
    else:
        print("No occurrences found in the heap.", file=sys.stdout)

    print("Done.", file=sys.stdout)


if __name__ == "__main__":
    main()
