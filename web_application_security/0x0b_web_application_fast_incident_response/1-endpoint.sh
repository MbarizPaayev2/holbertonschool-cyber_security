#!/bin/bash 
awk '{print $7}' log.txt | sort | uniq -c | sort -rn | head -n 1 | awk '{print $2}'
