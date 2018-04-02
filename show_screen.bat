
:loop
rem python runmyrobot/old_send_video.py 84736686 0 --screen-capture --kbps 250 --audio-input-device "Microphone (HD Webcam C270)"
python robotstreamer/old_send_video.py 203 0 --screen-capture --kbps 250 --audio-input-device "Microphone (HD Webcam C270)"
timeout 2
goto loop






