#!/bin/bash

# if [ ! -d "$config" ]; then printf '%s\n' "$config" >config.py fi;

until $(python3 -m index.py); do
    echo "Server 'myserver' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done