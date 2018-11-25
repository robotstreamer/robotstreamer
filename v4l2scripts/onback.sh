#!/bin/bash

#uncomment the next line to disable this command
#exit 0;
[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt
./decrement.sh tilt_absolute
v4l2-ctl -d "$device" -C tilt_absolute
