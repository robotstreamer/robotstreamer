#!/bin/bash

#this script prints the information in camcontrols in a user readable format

[ -e camcontrols.txt ] || ./getinfo.sh
source camcontrols.txt
declare outstr='' tempstr='' spaces='                    ';
declare -i index='0' max='0';
spaces+="$spaces";

max="${#controlnames[@]}";
echo 'NAME                               MIN         MAX         STEP        DEFAULT';
while [ "$index" -lt "$max" ];
do
  tempstr="${controlnames[index]}""$spaces";
  outstr="${tempstr:0:35}";
  tempstr="${controlmins[index]}""$spaces";
  outstr+="${tempstr:0:12}";
  tempstr="${controlmaxes[index]}""$spaces";
  outstr+="${tempstr:0:12}";
  tempstr="${controlsteps[index]}""$spaces";
  outstr+="${tempstr:0:12}";
  outstr+="${controldefaults[index]}";
  echo "$outstr";
  (( ++index ));
done;
echo -e '\n';


max="${#menunames[@]}";
index='0';
echo 'NAME                               OPTIONS             DEFAULT'
while [ "$index" -lt "$max" ];
do
  tempstr="${menunames[index]}""$spaces";
  outstr="${tempstr:0:35}";
  tempstr="${menuoptions[index]}""$spaces";
  outstr+="${tempstr:0:20}";
  outstr+="${menudefaults[index]}";
  echo "$outstr";
  (( ++index ));
done;

echo 'controlnames controlmins controlmaxes controlsteps controldefaults';
echo 'menunames menuoptions menudefaults';
