#!/bin/bash
find / -type d -perm  -xdev -0002 2>/dev/null exec chmod o-w {} + 
