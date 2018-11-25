#!/bin/bash

#uncomment the next line to disable this command
#exit 0;
[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt;

declare tbacklightcomp='';

read tbacklightcomp < <( v4l2-ctl -d "$device" -C backlight_compensation |
    cut -d ':' -f 2- | tr -d ' ' );

[ "$tbacklightcomp" -eq '0' ] &&
v4l2-ctl -d "$device" -c backlight_compensation=1 ||
v4l2-ctl -d "$device" -c backlight_compensation=0 ;

v4l2-ctl -d "$device" -C backlight_compensation;
