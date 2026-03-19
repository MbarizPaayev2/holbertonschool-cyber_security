#!/bin/bash
sudo nmap -sW $1 -p $2-$3 --exclude-ports 25-28 
