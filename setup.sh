#!/bin/sh

# if [ `du -sh  /tmp/filename.log` -gt 0 ]; then gzip /tmp/filename.log; fi
if [ ! -d "./venv" ]; then python3 -m venv venv; fi;
source ./venv/scripts/activate

python3 -m pip install -U pip
python3 -m pip install -U -r "requirements.txt"

python3 index.py