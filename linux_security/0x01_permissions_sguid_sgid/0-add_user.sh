#!/bin/bash
useradd "$1"
echo -n "$1:$2" | chpasswd
