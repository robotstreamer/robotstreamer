#import wave
#import contextlib
import uuid
import os
import tempfile

#def wavDuration(fname):
#
#        with contextlib.closing(wave.open(fname,'r')) as f:
#                frames = f.getnframes()
#                rate = f.getframerate()
#                duration = frames / float(rate)
#                return duration


def espeakBytes(message):

        tempDir = tempfile.gettempdir()
        
        tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
        outFilePath = os.path.join(tempDir, "out_" + str(uuid.uuid4()))

        f = open(tempFilePath, "w")
        f.write(message)
        f.close()
        
        os.system('cat ' + tempFilePath + ' | espeak -ven --stdout > ' + outFilePath)

        length = os.path.getsize(outFilePath)
        
        os.remove(tempFilePath)
        os.remove(outFilePath)

        return length

        

def main():
        #print('duration:', wavDuration('/home/pi/myaudio'))
        print('duration hello:', espeakBytes("hello"))
        print('duration hello world:', espeakBytes("hello world"))

        
if __name__ == "__main__":
        main()

        
