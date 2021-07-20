#!/bin/bash

if [ ! -d "$config" ]; then printf '%s\n' "$config" >config.py fi;


python3 -m index.py