import serial, string, time
import sqlite3

#!/usr/bin/env python3

#In this example /dev/ttyUSB0 is used
#This may change in your case to /dev/ttyUSB1, /dev/ttyUSB2, etc.


#The following block of code works like this:
#If serial data is present, read the line, decode the UTF8 data,
#...remove the trailing end of line characters
#...split the data into temperature and humidity
#...remove the starting and ending pointers (< >)
#...print the output

import serial
if __name__ == '__main__':
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    ser.flushOutput()
    ser.flushInput()

    while True:
        if ser.in_waiting > 0:
            rawserial = ser.readline()
            time.sleep(2)
            #cookedserial = rawserial.decode('utf-8').strip('\r\n')
            if rawserial[0].isdigit():
                print("Data Sesuai!")
                datasplit = rawserial.split(',')
                humidity  = float(datasplit[0])
                temperature = float(datasplit[1])
                print(temperature)
                print(humidity)
            elif rawserial.startswith(('-', '0x')):
                print("Ada Error!")
                print(rawserial)
            else:
                print(rawserial)
