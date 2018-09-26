#!/usr/bin/bash
declare installdirectory=$(pwd) userinput;
echo 'This script will install the dependencies for robotstreamer.';
echo 'You will be required to enter the password for root, because dnf requires root privileges to install packages.';
echo 'It will the download the source code from the robotstreamer github.';
echo 'This source code will be placed in the working directory: ';
echo "$installdirectory";
echo 'Type y and press enter to continue:'
read userinput;
[ "$userinput" == 'y' ] || exit;
su -c 'dnf --assumeyes install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm ;
dnf --assumeyes install git alsa-utils ffmpeg python3-devel python3-socketIO-client python3-pyserial espeak python3-i2c-tools python3-websockets;'
git clone https://github.com/robotstreamer/robotstreamer.git
