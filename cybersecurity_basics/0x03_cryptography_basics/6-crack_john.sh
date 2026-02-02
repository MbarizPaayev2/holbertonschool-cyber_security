#!/bin/bash
john $1  --format=Raw-SHA256 -w /usr/share/wordlists/rockyou.txt
