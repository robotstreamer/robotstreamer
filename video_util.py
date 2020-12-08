
import subprocess

def tryFFmpeg(num):
    command = f"ffmpeg -i /dev/video{num} -t 0.1 -framerate 10 -video_size 128d0x720 -f null -"
    print(command)
    if subprocess.call(command.split()) == 0:
        return True
    else:
        return False

def findWorkingVideoDevices():
    results = []
    for i in range(10):
        if tryFFmpeg(i):
            results.append(i)
    return results
    
if __name__ == "__main__":
    print(findWorkingVideoDevices())

    

