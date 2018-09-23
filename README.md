<h1> Open Robot Control Code For Connecting to RobotStreamer.com </h1>
<br>

RobotStreamer is a low latency live streaming platform. Stream from you desktop. Connect your movable cameras with TTS (robots) to *RobotStreamer.com*.

Broadcasters make the rules for their channels. Unlike most platforms, RobotStreamer is open to just about any content. Just maintain basic ethical decency, keep it legal, and keep it entertaining. For language, it's up to the broadcaster to decide how they want to moderate if at all.

You can create streams with Robots (movable cameras with TTS), that's our specialty, and you can also create tradional live IRL streams or game streams from the desktop. We currently use a different protocol than most live streaming platforms for lower latency.

We have a system called funbits that lets the streamers monetize their streams.

<h1> Desktop Live Stream: Installation </h1>

There are two ways to stream from your Desktop to RobotStreamer:

On desktop, you can stream using OBS and ffmpeg, follow instructions here:
https://github.com/robotstreamer/robotstreamer_win_obs

You can also stream directly using just ffmpeg although you may have issues with quality. Use instructions below but send_video_windows.py rather than just send_video.

Note that you'll want to visit the discord for questions and such. Streaming from Desktop is still a beta feature.
https://discord.gg/n6B7ymy








<h1> Robot Live Stream: Installation </h1>

RobotStreamer runs some software on your robot to connect to the server and send audio/video streams. If you'd like to order a robot, contact rick at rgiuly@gmail.com or you can make your own.

We typically test with Raspberry Pi on Raspian but you can use other hardware and OS's also if you know what you are doing.

Installation:

Copy this into the terminal, and follow the instructions.
This script has been tested on a Raspberry Pi 3, with a fresh flash of raspian stretch.

For Raspian Stretch:
```
sudo wget https://raw.githubusercontent.com/robotstreamer/robotstreamer/master/scripts/install.sh -O /tmp/install.sh && bash /tmp/install.sh
```

For Ubuntu 17.10 or later:
```
sudo wget https://raw.githubusercontent.com/robotstreamer/robotstreamer/master/scripts/install_ubuntu.sh -O /tmp/install_ubuntu.sh && bash /tmp/install_ubuntu.sh
```



After end installtion, all the files needed should be installed and ready for use, but you still need to change some arguments in your "/home/pi/start_robot" file, to make it suit your robot.


IMPORTANT: Particularly you need a stream key for controller.py and you should ask rgiuly@gmail.com for that. (We're working on making this easier so you don't have to ask.)
```
python controller.py --stream-key YOURKEYHERE ...
```
<img align="right" height=231 width=309 src="https://raw.githubusercontent.com/robotstreamer/images/master/robotstreamer_humanoid.jpg">


To edit your start_robot file, put this into the terminal.

```sudo nano /home/pi/start_robot```

<h2> Manual Install </h2>

<h3> Installing robot control and video scripts </h3>


The RasPi will need the following things install so it can talk to your motor and talk to the internet.

(1) Install [motor HAT software](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software):


(2) Install python serial, gnutls, python-dev, espeak, and python-smbus:

```apt-get install python-serial python-dev libgnutls28-dev espeak python-smbus python-pip git```


(3) Install socket.io client for python:

```pip install socketIO-client```

<img align="right" height=236 width=193 src="https://raw.githubusercontent.com/robotstreamer/images/master/robotstreamer_roomba.jpg">

(4) Install FFmpeg
sudo apt-get install ffmpeg


<h2> Robot Stream: Bring your Bot to life: Programs to run on the Raspberry Pi </h2>

Start by cloning the robotstreamer repository
```
cd ~
git clone https://github.com/robotstreamer/robotstreamer
cd robostreamer
```

Go to new robot page to create a robot. If you already have one, got to manage robots. There you'll find your Robot ID and Camera ID.

These two scripts need to be running in the background to bring your robot to life: controller.py, send_video.py. Here are instructions about how to start them.

Copy the 'start_robot' Script from robotstreamer/Scripts to the pi home folder

```cp ~/robotstreamer/scripts/start_robot ~/```

Edit the script so you can adjust some settings for controller.py and send_video.py:

```nano ~/start_robot```

Edit the YOURROBOTID to your robot ID.

Edit the YOURCAMERAID to your camera ID.

You are getting both IDs when you are creating a new bot on the website.

The second parameter on send_video.py 0 is assuming you have one camera plugged into your Pi and you are using it, which is usually the case.

There are more parameter possible for controller.py:

```robot_id```

Your Robot ID. Required

```--env prod | dev```

Environment for example dev or prod | default='prod'

```--type motor_hat | serial | l298n | motozero```

What type of motor controller should be used | default='motor_hat'

```--serial-device /dev/ttyACM0```

Serial device | default='/dev/ttyACM0'

```--male```

Use TTS with a male voice

```--female```

Use TTS with a female voice

```--voice-number 1```

What voice should be used | default=1

```--led max7219```

What LEDs should be used (if any) | default=none

```--ledrotate 180```

Rotates the LED matrix | default=none

Example start_robot:

```
cd /home/pi/robotstreamer
nohup scripts/repeat_start python controller.py YOURROBOTID --type motor_hat --male --voice-number 1 --led max7219 --ledrotate 180 &> /dev/null &
nohup scripts/repeat_start python send_video.py YOURCAMERAID 0 &> /dev/null &
```

<h3> Start script on boot </h3>
Use crontab to start the start_robot script on booting:

```
crontab -e
```

insert following line and save:

```
@reboot /bin/bash /home/pi/start_robot
```

That's it!

<h2> How does this work </h2>

We use ffmpeg to stream audio and socket.io to send control messages.

<h2> How to contribute </h2>

The is a community project. Making your own bot? Adding your own control stuff? Cool! We'd like to hear from you.


<h1> Hardware Compatibility </h1>

Adafruit Motor Hat

Serial Port based commands

GoPiGo

L298N

MotoZero

Missing something?, you can add it, open source!


<h1> Instructions for Specific Hardward Configurations </h1>

<h2> GoPiGo3 </h2>

For GoPiGo3, you will need to install the gopigo3 python module (which is different than older versions). It will need to be installed with the installation script from Dexter. Also, PYTHONPATH needs to be set to "/home/pi/Dexter/GoPiGo3/Software/Python"

Refer to this:
https://github.com/DexterInd/GoPiGo3
```
sudo git clone http://www.github.com/DexterInd/GoPiGo3.git /home/pi/Dexter/GoPiGo3
sudo bash /home/pi/Dexter/GoPiGo3/Install/install.sh
sudo reboot
```

If you need to update the firmware:
```
cd Dexter/GoPiGo3/Firmware
chmod +x gopigo3_flash_firmware.sh
./gopigo3_flash_firmware.sh
```

Reference:

https://www.dexterindustries.com/GoPiGo/get-started-with-the-gopigo3-raspberry-pi-robot/test-and-troubleshoot-the-gopigo3-raspberry-pi-robot/


<h2> High Level Overview </h2>

The robot communicates with our control server via websockets. It communicates with our audio and video stream servers via http stream. Users connect to our servers.

The robot client connects via websockets to the API service to retrieve configuration information, to the chat to receive chat messages, the video/audio relays to send its camera and microphone capture, and to the control service to receive user commands.

<h2>Interfaces: </h2>
Control server via websockets
Chat server via websockets
Sends video stream via websockets
Sends audio stream via websockets

<h2>Responsibilities: </h2>
Capturing Audio and Video
Relays commands to robot hardware
Text to Speech
Supports remote login for diagnostics and updates
Configuration updates from the web client (partially implemented)

<h2>Detailed Description: </h2>
The robot client connects to four external services: API Service, Chat Service, Video/Audio Service, and the Control Service.

<h4>API Service</h4>
Provides information about which host and port to connect to for the chat service, video/audio service, and control service

<h4>Chat Service</h4>
Relays chat messages sent from the web clients to the robot

<h4>Video/Audio Service</h4>
The robot client streams ffmpeg output to the video/audio service

<h4>Control Service</h4>
Relays control messages sent from the web clients to the robot





