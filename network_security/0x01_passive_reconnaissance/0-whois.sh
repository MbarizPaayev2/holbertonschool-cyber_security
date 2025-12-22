#!/bin/bash 
whois $1 | awk '{print $1,$9}' -f $1.csv
