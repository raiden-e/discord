#!/bin/bash

printf '%s\n' "$config" >config.py

python3 -m index.py