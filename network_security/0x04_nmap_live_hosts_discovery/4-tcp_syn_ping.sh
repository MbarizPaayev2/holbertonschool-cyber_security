#!/bin/bash 
sudo nmap -sn $1 -PS 22,80,443
