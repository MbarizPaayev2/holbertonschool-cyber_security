#!/bin/bash
sudo nmap -sF -p 80-85 -f $1 -T2
