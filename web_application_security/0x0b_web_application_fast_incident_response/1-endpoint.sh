#!/bin/bash
awk '{print $7}' "$1" | sort | uniq -c | sort -rn | head -n 1 | awk '{print $2}'
