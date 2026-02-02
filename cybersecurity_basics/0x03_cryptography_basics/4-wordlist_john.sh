#!/bin/bash
john $1 -w /usr/share/wordlists/rockyou.txt 
john --show "$1" | cut -d: -f2 | head -n -1 > 4-password.txt
