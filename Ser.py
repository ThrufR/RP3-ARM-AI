import os
from typing import Optional

import serial
import struct
import time

ser = serial.Serial('COM4', baudrate=9600)


def sendtoarduino():
    x = int(input())
    x1 = int(input())
    x2 = int(input())
    #x3 = int(input())
    message = struct.pack('<iii', x, x1, x2)
    print('piez') #For debugging process
    try:
        ser.write(message)
        ser.flush()
    except:
        ser.close()
        ser.open()
        ser.write(message)
        print("error occured")
    print(message)



pass


def main():
    while(True):
        print("Wprowadź kod")
        m = input()
        if m == '1':
            sendtoarduino()

main()

