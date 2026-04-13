#!/bin/bash
grep -E "iptables" auth.log | grep -E "A INPUT" | sort | uniq -c | wc -l
