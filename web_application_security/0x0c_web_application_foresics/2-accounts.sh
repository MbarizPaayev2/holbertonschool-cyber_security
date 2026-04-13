#!/bin/bash
tail -n 1000 $1 | grep "Failed" | awk '{print $9}' | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'
