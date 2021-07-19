#!/usr/bin/env python

import sqlite3
import serial, string, time, datetime, dateutil.parser
import sys, os
from time import strftime, localtime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)

# Google Docs spreadsheet name.
spreadsheet_name = 'sensors-data_TA'
account_sid = os.getenv('TWILIO_ACCOUNT_SID') #'AC5cadcf435cb0ef40929a86677e341936'
auth_token = os.getenv('TWILIO_AUTH_TOKEN') #'e2e9009e6ceb35603c50bb6149c1c5ef'
client = Client(account_sid, auth_token)

def sent_alert(temp):
    if last_sent == 'Not Set': 
        message = client.messages.create(
                                body='PERINGATAN DINI BENCANA, SUHU MENCAPAI {} °C!'.format(temp),
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+6281933033531'
                            )
        date_sent = datetime.datetime.now()
        os.environ['LAST_SENT'] = str(date_sent)
        #tulis ke env variabel  'LAST_SENT'
    else : #last_sent is not None
        date_now = datetime.datetime.now()
        datetime_last = dateutil.parser.parse(last_sent)
        #datetime_last = datetime.strptime(last_sent, "%d/%m/%y %H:%M:%S.%f")
        difference = date_now - datetime_last
        delta = difference // datetime.timedelta(seconds=1)
        int_delta = int(delta)
        if delta >= 180 :
            print('Selesai')
            message = client.messages.create(
                                body='PERINGATAN DINI BENCANA, SUHU MENCAPAI {} °C!'.format(temp),
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+6281933033531'
                            )
            date_sent = datetime.datetime.now()
            os.environ['LAST_SENT'] = str(date_sent)
        #else :
            #return None
    #else :
        #return None


def log_values(sensor_id, hum, temp, err):
      conn=sqlite3.connect('/var/www/TA_AdminLTE/lab_app.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
      curs=conn.cursor()
      curs.execute("""INSERT INTO sensors values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?), (?), (?), 0)""", (sensor_id,hum,temp,err))  #This will store the new record at UTC
      conn.commit()
      scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
      creds = ServiceAccountCredentials.from_json_keyfile_name('/var/www/TA_AdminLTE/raspberry-pi-data-logger-9434d437f6f7.json', scope)
      client = gspread.authorize(creds)
      sheet = client.open(spreadsheet_name).sheet1
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
   last_sent = os.environ.get('LAST_SENT', 'Not Set')
   if ser.in_waiting > 0:
      rawserial = ser.readline()
      serial_str = rawserial.decode('ISO-8859-1').strip('\r\n')
      if serial_str[0].isdigit():
         print("Data Sesuai!")
         print(serial_str)
         datasplit = serial_str.split(',')
         humidity =  '{:.2f}'.format(float(datasplit[0]))
         hum_float = float(humidity)
         temperature =  '{:.2f}'.format(float(datasplit[1]))
         temp_float = float(temperature)
         if (temp_float >= 35.00):
             sent_alert(temperature)
         print(temperature)
         print(humidity)
         log_values("1", humidity, temperature, None)
      elif serial_str.startswith(('-', '0x')):
         print("Ada Error!")
         print(serial_str)
         error = float(serial_str)
         log_values("1", None, None, error)
      else:
         print(serial_str)
      #break
      ser.flushOutput()
      ser.flushInput()      
   #time.sleep(0.1)


#row = [strftime("%Y-%m-%d %H:%M:%S", localtime()),sensor_id,round(temp,2),round(hum,2),""]
#time.sleep(2)
#cookedserial = rawserial.decode('utf-8').strip('\r\n')
#print(rawserial)
#print(humidity)
#humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)

# If you don't have a sensor but still wish to run this program, comment out all the
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
# import random
# humidity = random.randint(1,100)
# temperature = random.randint(10,30)
#if humidity is not None and temperature is not None:
#	log_values("1", temperature, humidity)
#else:
#	log_values("1", -999, -999)
