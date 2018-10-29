#!/bin/bash

#searches controlnames[] for a control with the name of $1
#if it finds it it prints the index to stdout
#if it isn't found it prints -1 to stdout
fngetcontrol(){
  source camcontrols.txt;
  declare -i index='0' max="${#controlnames[@]}";

  while [ "$index" -lt "$max" ];
  do
    if [ "${controlnames[index]}" == "$1" ];
    then
      echo "$index";
      return '0';
    else
      (( ++index ));
    fi;
  done;
  echo '-1';

  return 1;
};

#searches menunames[] for a control with the name of $1
#if it finds it it prints the index to stdout
#if it isn't found it prints -1 to stdout
fngetmenu(){
  source camcontrols.txt;
  declare -i index='0' max="${#menunames[@]}";

  while [ "$index" -lt "$max" ];
  do
    if [ "${menunames[index]}" == "$1" ];
    then
      echo "$index";
      return '0';
    else
      (( ++index ));
    fi;
  done;
  echo '-1';

  return 1;
};
