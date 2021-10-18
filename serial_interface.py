import serial
import robot_util

try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
except Exception as e:
    print("Serial Error, Failed to connect.", e)

def handleCommand(command, keyPosition, price=0):
    print("Sending command to serial device")
    ser.write(command.encode())