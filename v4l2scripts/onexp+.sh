#!/bin/bash

#uncomment the next line to disable this command
#exit 0;
[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt;
v4l2-ctl -d "$device" -c exposure_auto=1
./increment.sh exposure_absolute
v4l2-ctl -d "$device" -C exposure_absolute
