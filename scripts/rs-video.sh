#!/bin/bash

#usage: fngetaudioport <robot id>
fngetvideoport(){
  declare -r porturl='http://robotstreamer.com:6001/v1/get_endpoint/jsmpeg_video_capture/'"$1";
  declare  port;

  read port < <( wget -O - "$porturl" 2> /dev/null | head -n 1 |
      egrep -o '"port" *: *[0-9]+' | tr -dc '0-9' );
  if [ ${#port} -lt '1' ];
  then
    return '1';
  else
    echo "$port";
    return '0';
  fi;
  return '2';
};


#print help message
fnhelp(){
  declare line;

  declare -ra helpmessage=(
  'This script requires ffmpeg and wget. It will stream from an x11 display to'
  'a given camera id. It is designed to be used with the keepalive.py script'
  'and rs-movie.sh. You must be sending the keep alive signal or '
  'robotstreamer.com will not allow you to stream to your camera.'
  'Usage: rs-audio.sh -h'
  '       prints this help message'
  'Usage: rs-video.sh <camera id> <display> <fps> <hres> <vres>'
  '       Camera id is given to you by robot streamer. If you do not know yours'
  '       ask in discord.'
  '       Display is your x11 display number. It is a non-negative integer. It'
  '       can usually be found by running echo $DISPLAY.'
  '       fps is how many frames per second you want to stream.'
  '       hres is the horizontal resolution of your screen.'
  '       vres is the vertical resolution of your screen.' );

  for line in "${helpmessage[@]}";
  do
    echo "$line";
  done;

  return '0';
};

if [ "$1" == '-h' ];
then
  fnhelp;
  exit '0';
fi;
if [ "$#" -lt '5' ];
then
  echo 'Not enough arguments.' >&2;
  fnhelp >&2;
  exit '1';
fi;
if [ "$#" -gt '5' ];
then
  echo 'Too many arguments.' >&2;
  fnhelp >&2;
  exit '1';
fi;
if ! which ffmpeg &>/dev/null;
then
  echo 'Could not find ffmpeg.' >&2;
  fnhelp >&2;
  exit '2';
fi;

declare port='';
read port < <( fngetvideoport "$1" );
if [[ "$port" =~ ^[0-9]+$ ]];
then
  declare res="$4"'x'"$5";
  declare x11grabarg="$2"'+0,0';
  declare videoendpoint='http://robotstreamer.com:'"$port"'/hellobluecat/1280/720/';
  declare -a ffmpegargs=( '-hide_banner'
      '-video_size' "$res"
      '-framerate' "$3"
      '-f' 'x11grab' '-i' "$x11grabarg" '-f' 'mpegts'
      '-codec:v' 'mpeg1video' '-s' "$res" '-b:v' '1200k'
      '-bf' '0' '-muxdelay' '0.001'
      "$videoendpoint"
  );
  ffmpeg "${ffmpegargs[@]}";
else
  echo 'Trouble getting video endpoint port.' >&2;
  echo 'port='"$port" >&2;
  fnhelp >&2;
  exit '3';
fi;

