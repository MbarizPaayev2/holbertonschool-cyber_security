#!/bin/bash
#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt "$1" > /dev/null && john --show "$1" | grep ":" | cut -d: -f2 > 4-password.txt
