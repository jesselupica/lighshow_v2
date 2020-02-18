#!/bin/bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo python3 src/lightshow.py "$@"
else 
    sudo pigpiod && cd src/ && sudo python3 /home/pi/Public/lighshow_v2/src/lightshow.py
fi 