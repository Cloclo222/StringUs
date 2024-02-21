import serial
import time

arduino = serial.Serial(port='COM11',   baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x,   'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return   data


while True:
    num1 = input("Angle 1: ")
    angle1 = num1
    num2 = input("Angle 2: ")
    angle2 = num2

    concat = f'{num1}, {num2}.'
    #print(concat)

    value   = write_read(concat)
    print(value)
