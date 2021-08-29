#!/bin/sh

kill $(pgrep -f 'python3 -m index.py')
git pull
python3 -m pip install -U pip
python3 -m pip install -U -r "requirements.txt"

# if [ ! -d "$config" ]; then printf '%s\n' "$config" >config.py fi;

# until $(python3 -m index.py); do
#     echo "Server 'myserver' crashed with exit code $?.  Respawning.." >&2
#     sleep 1
# done

python3 -m index.py
