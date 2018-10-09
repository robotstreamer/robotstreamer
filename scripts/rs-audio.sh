#!/bin/bash

#usage: fngetaudioport <robot id>
fngetaudioport(){
  declare -r porturl='http://robotstreamer.com:6001/v1/get_endpoint/jsmpeg_audio_capture/'"$1";
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
  'This script requires ffmpeg, wget, and pulseaudio. It will stream from any'
  'pulseaudio source to a given camera id. It is designed to be used with the'
  'keepalive.py script and rs-movie.sh. You must be sending the keep alive'
  'signal or robotstreamer.com will not allow you to stream to your camera.'
  'Usage: rs-audio.sh -h'
  '       prints this help message'
  'Usage: rs-audio.sh <camera id> <pulse audio source>'
  '       Camera id is given to you by robot streamer. If you do not know yours'
  '       ask in discord.'
  '       A list of possible pulse audio sources can be found by using running:'
  '       pactl list sources | grep Name'
  'A list of currently detected audio sources:' );

  for line in "${helpmessage[@]}";
  do
    echo "$line";
  done;
  which pactl &> /dev/null &&  pactl list sources | grep Name;

  return '0';
};

if [ "$1" == '-h' ];
then
  fnhelp;
  exit '0';
fi;
if [ "$#" -lt '2' ];
then
  echo 'Not enough arguments.' >&2;
  fnhelp >&2;
  exit '1';
fi;
if [ "$#" -gt '2' ];
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
read port < <( fngetaudioport "$1" );
if [[ "$port" =~ ^[0-9]+$ ]];
then
  declare audioendpoint='http://robotstreamer.com:'"$port"'/hellobluecat/640/480';
  declare -a ffmpegargs=( '-hide_banner'
      '-f' 'pulse' '-ar' '44100' '-ac' '2' '-i' "$2" '-f' 'mpegts'
      '-codec:a' 'mp2' '-b:a' '192k'
      '-muxdelay' '0.001' "$audioendpoint" );

  ffmpeg "${ffmpegargs[@]}";
else
  echo 'Trouble getting audio endpoint port.' >&2;
  echo 'port='"$port" >&2;
  fnhelp >&2;
  exit '3';
fi;
