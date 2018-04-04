echo first parameter camera id
#:loop
py -2 send_video_windows.py %1 0 --screen-capture --kbps 300 --audio-input-device "Microphone (HD Webcam C270)"
#timeout 5
#goto loop






