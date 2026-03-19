#!/bin/bash
sudo nmap -sM $1  -p 22,80,443,21,23 -vv 
