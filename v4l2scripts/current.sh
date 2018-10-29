#!/bin/bash

#prints the current values for v4l2 controls

[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt;

declare -a controlarray=( "${controlnames[@]}" "${menunames[@]}" );
declare name='' list="$controlarray";
for name in "${controlarray[@]:1}";
do
  list="$list"','"$name";
done;
v4l2-ctl -d "$device" -C "$list"
