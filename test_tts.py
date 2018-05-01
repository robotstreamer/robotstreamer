import os

for i in (0, 1, 2):
    cmd = "echo pooooooo1 | espeak -ven --stdout | aplay -D plughw:%d,0" % i
    print(cmd)
    os.system(cmd)


    
