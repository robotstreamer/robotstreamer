#!/bin/bash

#uncomment the next line to disable this command
#exit 0;
[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt;
v4l2-ctl -d "$device" -c white_balance_temperature_auto=0;
./decrement.sh white_balance_temperature;
v4l2-ctl -d "$device" -C white_balance_temperature;
