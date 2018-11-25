#!/bin/bash

#This script creates camcontrols.txt. camcontrols.txt contains a lot of info
#about the device to prevent wasting a lot of time querying v4l2 and parsing
#every time a command is sent from the control server. Putting this info in a
#file also gives the user a convenient place to edit the step, minimum, and
#maximum values.

#Edit this variable to change the webcam device that this operates on. You will
#need to delete camcontrols.txt for the changes to take effect.
declare webcamdevfile='/dev/video0';

fngetinfo(){
  declare device="$1"
  declare -a lines=( );
  declare -a controlnames=( ) controlmins=( ) controlmaxes=( ) controlsteps=( );
  declare -a controldefaults=( ) menunames=( ) menuoptions=( ) menudefaults=( );
  declare -i max='0' index='0' endbool='0' controlmenu='0';
  declare -i  controlmin='0' controlmax='0' controlstep='0' controldefault='0';
  declare controlname='' lineholder='' outstr='';

  readarray -t lines < <(
      v4l2-ctl -L -d "$device" | tr '\t' ' ' | tr -s ' ' | egrep -o '[^ ].*$' );
  max="${#lines[@]}"
  while [ "$index" -lt "$max" ];
  do
    lineholder="${lines[index]}";
    if [[ "$lineholder" =~ \(int\)\ *: ]];
    then
      read controlname < <( echo "$lineholder" | cut -d ' ' -f '1' );
      read controlstep < <( echo "$lineholder" | cut -d ':' -f '2-' |
           egrep -o 'step=-?[0-9]+' | cut -d '=' -f '2-' );
      read controlmin < <( echo "$lineholder" | cut -d ':' -f '2-' |
          egrep -o 'min=-?[0-9]+' | cut -d '=' -f '2-' );
      read controlmax < <( echo "$lineholder" | cut -d ':' -f '2-' |
          egrep -o 'max=-?[0-9]+' | cut -d '=' -f '2-' );
      read controldefault < <( echo "$lineholder" | cut -d ':' -f '2-' |
          egrep -o 'default=-?[0-9]+' | cut -d '=' -f '2-' );

      controlnames=( "${controlnames[@]}" "$controlname" );
      controlmins=( "${controlmins[@]}" "$controlmin" )
      controlmaxes=( "${controlmaxes[@]}" "$controlmax" )
      controlsteps=( "${controlsteps[@]}" "$controlstep" )
      controldefaults=( "${controldefaults[@]}" "$controldefault" )
      (( ++index ));
    elif [[ "$lineholder" =~ \(bool\)\ *: ]];
    then
      read controlname < <( echo "$lineholder" | cut -d ' ' -f '1' );
      read controldefault < <( echo "$lineholder" | cut -d ':' -f 2- |
          egrep -o 'default=-?[0-9]+' | cut -d '=' -f '2-' );
      controlnames=( "${controlnames[@]}" "$controlname" );
      controlmins=( "${controlmins[@]}" '0' )
      controlmaxes=( "${controlmaxes[@]}" '1' )
      controlsteps=( "${controlsteps[@]}" '1' )
      controldefaults=( "${controldefaults[@]}" "$controldefault" )
      (( ++index ));
    elif [[ "$lineholder" =~ \(menu\)\ *: ]];
    then
      read controlname < <( echo "$lineholder" | cut -d ' ' -f '1' );
      read controldefault < <( echo "$lineholder" | cut -d ':' -f 2- |
          egrep -o 'default=-?[0-9]+' | cut -d '=' -f '2-' );
      menunames=( "${menunames[@]}" "$controlname" );
      menudefaults=( "${menudefaults[@]}" "$controldefault" );
      outstr='';
      endbool='0';
      while [ "$endbool" -eq '0' ] && [ "$index" -lt "$max" ] ;
      do
        (( ++index ));
        lineholder="${lines[index]}";
        if [[ "$lineholder" =~ ^[0-9]+:.*$ ]];
        then
          read controlmenu < <( echo "$lineholder" | cut -d ':' -f '1' );
          if [ "${#outstr}" -eq '0' ];
          then
            outstr="$controlmenu";
          else
            outstr="$outstr"' '"$controlmenu";
          fi;
        else
          endbool='1';
        fi;
      done;
      menuoptions=( "${menuoptions[@]}" "$outstr" );
    else
      (( ++index ));
    fi;
  done;
  declare -p controlnames controlmins controlmaxes > camcontrols.txt;
  declare -p  controlsteps controldefaults menunames >> camcontrols.txt;
  declare -p menudefaults menuoptions >> camcontrols.txt;
  declare -p device >> camcontrols.txt
};

fngetinfo "$webcamdevfile";
