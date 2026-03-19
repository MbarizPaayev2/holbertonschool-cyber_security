#!/bin/bash
sudo nmap -sM $1  -p 21,22,23,80,443  -vvv
