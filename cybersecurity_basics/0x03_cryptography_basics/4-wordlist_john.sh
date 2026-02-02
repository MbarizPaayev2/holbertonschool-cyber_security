#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt "$1" | john --show "$1" | grep ":" | cut -d: -f2 > 4-password.txt
