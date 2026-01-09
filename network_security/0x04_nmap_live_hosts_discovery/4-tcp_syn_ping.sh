#!/bin/bash 
sudo nmap -sn $1 -PS22,80,443
