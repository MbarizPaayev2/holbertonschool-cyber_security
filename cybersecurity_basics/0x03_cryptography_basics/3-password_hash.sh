#!/bin/bash
echo -n "$1" | openssl dgst -sha512 > 3_hash.txt
