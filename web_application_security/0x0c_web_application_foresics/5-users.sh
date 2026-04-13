#!/bin/bash
grep -E "new user" auth.log |awk '{sub("name=", "", $8); sub(",", "", $8); print $8}'| sort | uniq | paste -sd,
