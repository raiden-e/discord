#!/bin/sh

kill $(pgrep -f 'python3 index.py')
git pull
python3 -m pip install -U pip
python3 -m pip install -U -r "requirements.txt"

bash run.sh