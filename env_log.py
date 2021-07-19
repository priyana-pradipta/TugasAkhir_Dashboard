#!/usr/bin/env python

import sqlite3
import serial, string, time
import sys
from time import strftime, localtime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
logging.basicConfig(level=logging.INFO)

# Google Docs spreadsheet name.
spreadsheet_name = 'sensors-data_TA'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/var/www/TA_AdminLTE/raspberry-pi-data-logger-9434d437f6f7.json', scope)
client = gspread.authorize(creds)
sheet = client.open(spreadsheet_name).sheet1

def log_values(sensor_id, hum, temp, err):
      conn=sqlite3.connect('/var/www/TA_AdminLTE/lab_app.db')
      curs=conn.cursor()
      curs.execute("""INSERT INTO sensors values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?), (?), (?), 0)""", (sensor_id,hum,temp,err))
      conn.commit()
      curs.execute("""SELECT * FROM sensors WHERE uploaded IN ('0') ORDER BY rDatetime ASC""")
      results = curs.fetchall()
      for val in results : 
            try :
               if (val[2] == None) and (val[3] == None) :
                  row = [val[0],val[1],"","",val[4]]
               else :
                  row = [val[0],val[1],val[2],val[3],""]

               sheet.append_row(row)
            except KeyboardInterrupt :
               conn.close()
               sys.exit()
               pass
            except gspread.exceptions.GSpreadException as e :
               logging.error('Unexpected error: {0}'.format(e))
            except gspread.exceptions.APIError as e :
               logging.error('Unexpected error: {0}'.format(e))
            curs.execute("""UPDATE sensors SET uploaded = '1' WHERE rDatetime IN (?)""", [val[0]])
            conn.commit()

      conn.close()

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
      cookedserial = rawserial.decode('ISO-8859-1').strip('\r\n')
      #rawserial_str = str(rawserial)
      if cookedserial[0].isdigit():
         print("Data Sesuai!")
         print(cookedserial)
         datasplit = cookedserial.split(',')
         humidity =  '{:.2f}'.format(float(datasplit[0]))
         temperature =  '{:.2f}'.format(float(datasplit[1]))
         print(temperature)
         print(humidity)
         log_values("1", humidity, temperature, None)
      elif cookedserial.startswith(('-', '0x')):
         print("Ada Error!")
         print(cookedserial)
         error = float(cookedserial) 
         log_values("1", None, None, error)
      else:
         print(cookedserial)
      ser.flushOutput()
      ser.flushInput()
   #time.sleep(0.1)

