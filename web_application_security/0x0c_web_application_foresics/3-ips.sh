#!/bin/bash
grep "Accepted" $1 | awk '{print $11}' | sort | uniq | wc -l
