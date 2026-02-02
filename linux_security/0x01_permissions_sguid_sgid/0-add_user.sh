#!/bin/bash
adduser "$1"
echo -n "$1:$2" | chpasswd
