#!/bin/bash
sudo nmap -p $2  --host-timeout 1000ms  -sA  $1 --reason
