# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         #messaging_service_sid='MG63903ed499ce8b64785d490ee9105490 ',
         body='Waspada Bencana',
         from_='+14439607383',
         to='+6281933033531'
     )

print(message.sid)