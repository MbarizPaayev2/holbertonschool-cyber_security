#!/bin/bash
sudo nmap --scanflags SYNACKFINRSTPSHURG $1 -p $2 -oN custom_scan.txt
