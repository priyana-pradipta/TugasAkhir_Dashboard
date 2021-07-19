import serial, string, time
import sqlite3

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
