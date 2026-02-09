#!/bin/bash
showmount -e "$1" 2>/dev/null | awk '$2=="*" {print "[OPEN] "$1": "$0}'
