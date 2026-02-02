#!/bin/bash
echo -n "$1" | openssl rand -hex 8 dgst -sha512 > 3_hash.txt
