#!/bin/bash

#uncomment the next line to disable this command
#exit 0;
[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt;
v4l2-ctl -d "$device" -c focus_auto=0
./increment.sh focus_absolute
v4l2-ctl -d "$device" -C focus_absolute
