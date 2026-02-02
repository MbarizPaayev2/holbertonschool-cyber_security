#!/bin/bash
sudo tee /etc/sudoers.d/$1 <<< "$1 ALL=(ALL) NOPASSWD: ALL"
