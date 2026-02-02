#!/bin/bash 
hashcat -m 0 -a 0 /usr/share/wordlists/rockyou.txt "$1"  --show
