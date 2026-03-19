#!/bin/bash
sudo nmap -sX --open --reason --packet-trace  -p 440-450  $1
