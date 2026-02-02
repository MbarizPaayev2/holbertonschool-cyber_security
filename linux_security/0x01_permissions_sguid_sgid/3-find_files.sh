#!/bin/bash
find / -perm -exec  -4000 2>/dev/null | ls -la 
