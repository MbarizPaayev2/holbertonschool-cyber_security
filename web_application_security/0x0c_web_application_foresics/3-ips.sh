#!/bin/bash
grep "Accepted password for root" auth.log | awk '{print $11}' |sort | uniq -c | sort -nr | wc -l
