#!/bin/bash
nmap -sV -p 80,443 --script=vulners "$1"
