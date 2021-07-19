# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID') #'AC5cadcf435cb0ef40929a86677e341936'
auth_token = os.getenv('TWILIO_AUTH_TOKEN') #'e2e9009e6ceb35603c50bb6149c1c5ef'
client = Client(account_sid, auth_token)
temp = 45

message = client.messages.create(
                              body='Waspada Bancana!, suhu mencapai {}'.format(temp),
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+6281933033531'
                          )

print(message.sid)