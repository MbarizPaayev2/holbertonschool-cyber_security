#!/bin/bash
sudo echo /etc/sudoers.d/$1 <<< "$1 ALL=(ALL) NOPASSWD: ALL"
