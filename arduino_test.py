import serial
import time

arduino = serial.Serial('/dev/cu.usbmodem14401', 9600) 
time.sleep(2)


test_emotions = ['h', 's', 'a', 'f', 'n']

for char in test_emotions:
    print("Sending emotion " + char)
    arduino.write(char.encode())
    time.sleep(2)
