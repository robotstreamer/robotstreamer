import sys
import time
import robot_util
sys.path.append("/home/pi/Dexter/GoPiGo3/Software/Python")
import easygopigo3
easyGoPiGo3 = easygopigo3.EasyGoPiGo3()



def handleCommand(command, keyPosition, price=0):

    # only uses pressing down of keys
    if keyPosition != "down":
        return

    print("handle command", command, keyPosition)
    e = easyGoPiGo3
    if command == 'L':
        e.set_motor_dps(e.MOTOR_LEFT, -e.get_speed())
        e.set_motor_dps(e.MOTOR_RIGHT, e.get_speed())
        time.sleep(0.15)
        easyGoPiGo3.stop()
    if command == 'R':
        e.set_motor_dps(e.MOTOR_LEFT, e.get_speed())
        e.set_motor_dps(e.MOTOR_RIGHT, -e.get_speed())
        time.sleep(0.15)
        easyGoPiGo3.stop()
    if command == 'F':
        easyGoPiGo3.forward()
        time.sleep(0.35)
        easyGoPiGo3.stop()
    if command == 'B':
        easyGoPiGo3.backward()
        time.sleep(0.35)
        easyGoPiGo3.stop()
        
    robot_util.handleSoundCommand(command, keyPosition, price)
