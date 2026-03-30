#!/usr/bin/env python3
"""
read_write_heap.py

Usage: read_write_heap.py <pid> <search_string> <replace_string>

- Finds the heap region(s) of the process via /proc/<pid>/maps
- Searches only in readable+writable heap memory for the exact ASCII search_string
- Replaces all non-overlapping occurrences with replace_string (must be same length or shorter)
- If lengths differ, it pads with null bytes or truncates accordingly (but prefers same length for simplicity)
- Prints interesting info: number of replacements, addresses where changes happened
- Requires root/sudo for /proc/<pid>/mem access in most cases
"""

import sys
import re
import os

def usage_error(msg):
    print(f"Error: {msg}", file=sys.stdout)
    print("Usage: read_write_heap.py pid search_string replace_string", file=sys.stdout)
    print("       pid: integer process ID", file=sys.stdout)
    print("       strings must be ASCII", file=sys.stdout)
    sys.exit(1)

def main():
    if len(sys.argv) != 4:
        usage_error("Incorrect number of arguments")

    try:
        pid = int(sys.argv[1])
    except ValueError:
        usage_error("PID must be an integer")

    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    if not search_str or not replace_str:
        usage_error("Search and replace strings cannot be empty")

    # Convert to bytes (ASCII)
    try:
        search_bytes = search_str.encode('ascii')
        replace_bytes = replace_str.encode('ascii')
    except UnicodeEncodeError:
        usage_error("Strings must be valid ASCII")

    if len(replace_bytes) > len(search_bytes):
        print("Warning: replace_string is longer than search_string. Extra bytes will be ignored.", file=sys.stdout)

    maps_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    if not os.path.exists(maps_path):
        usage_error(f"Process with PID {pid} not found or no permission to access /proc/{pid}")

    heap_regions = []

    # Parse /proc/pid/maps to find heap (look for [heap] or rw-p anonymous regions that are likely heap)
    try:
        with open(maps_path, 'r') as f:
            for line in f:
                # Example line: 555e646e0000-555e646e3000 rw-p 00000000 00:00 0          [heap]
                parts = line.split()
                if len(parts) < 2:
                    continue
                addr_range = parts[0]
                perms = parts[1]
                pathname = parts[-1] if len(parts) > 5 else ""

                if 'rw' not in perms:  # Must be readable and writable
                    continue

                # Heap is usually marked [heap], or the main anonymous rw-p region after the binary
                if pathname == '[heap]' or (not pathname.startswith('/') and 'heap' in line.lower()):
                    try:
                        start, end = map(lambda x: int(x, 16), addr_range.split('-'))
                        heap_regions.append((start, end))
                    except ValueError:
                        continue
    except Exception as e:
        usage_error(f"Failed to read {maps_path}: {e}")

    if not heap_regions:
        print(f"Warning: No heap region found for PID {pid}. Searching all rw anonymous regions instead.", file=sys.stdout)
        # Fallback: search all rw-p anonymous regions
        with open(maps_path, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) < 2:
                    continue
                addr_range = parts[0]
                perms = parts[1]
                pathname = parts[-1] if len(parts) > 5 else ""
                if 'rw-p' in perms and not pathname.startswith('/'):
                    try:
                        start, end = map(lambda x: int(x, 16), addr_range.split('-'))
                        heap_regions.append((start, end))
                    except ValueError:
                        continue

    if not heap_regions:
        usage_error(f"No suitable rw heap/anonymous regions found for PID {pid}")

    replacements = 0
    changed_addresses = []

    try:
        with open(mem_path, 'rb+') as mem_file:  # rb+ for read/write
            for start, end in heap_regions:
                size = end - start
                if size <= 0:
                    continue

                print(f"Scanning heap region: 0x{start:x} - 0x{end:x} ({size} bytes)", file=sys.stdout)

                # Read the entire region (be careful with very large heaps)
                mem_file.seek(start)
                try:
                    data = mem_file.read(size)
                except OSError:
                    print(f"  Skipping region (permission/I/O error)", file=sys.stdout)
                    continue

                # Find all occurrences (non-overlapping)
                pos = 0
                while True:
                    pos = data.find(search_bytes, pos)
                    if pos == -1:
                        break

                    abs_addr = start + pos

                    # Prepare replacement (truncate or pad with \0 if lengths differ)
                    repl = replace_bytes[:len(search_bytes)]
                    if len(repl) < len(search_bytes):
                        repl += b'\x00' * (len(search_bytes) - len(repl))

                    # Write back
                    mem_file.seek(abs_addr)
                    mem_file.write(repl)

                    replacements += 1
                    changed_addresses.append(abs_addr)

                    print(f"  Replaced at 0x{abs_addr:x}: '{search_str}' -> '{replace_str}'", file=sys.stdout)

                    pos += len(search_bytes)  # move past this match (non-overlapping)

    except PermissionError:
        usage_error(f"Permission denied accessing /proc/{pid}/mem. Run with sudo.")
    except Exception as e:
        print(f"Error during memory operation: {e}", file=sys.stdout)
        sys.exit(1)

    # Summary
    print("\n=== Summary ===", file=sys.stdout)
    print(f"Process PID: {pid}", file=sys.stdout)
    print(f"Search string: '{search_str}'", file=sys.stdout)
    print(f"Replace string: '{replace_str}'", file=sys.stdout)
    print(f"Heap regions scanned: {len(heap_regions)}", file=sys.stdout)
    print(f"Replacements made: {replacements}", file=sys.stdout)

    if changed_addresses:
        print("Changed addresses:", file=sys.stdout)
        for addr in changed_addresses:
            print(f"  0x{addr:x}", file=sys.stdout)
    else:
        print("No occurrences of the search string found in the heap.", file=sys.stdout)

    print("Done.", file=sys.stdout)


if __name__ == "__main__":
    main()
