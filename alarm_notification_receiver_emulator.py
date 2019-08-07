import base64
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

MQTT_SERVER_FLESPI = 'mqtt.flespi.io'
MQTT_TOKEN_FLESPI = 'FlespiToken ' \
                    'R4XF03Rp3KStynVTDRrOuju7odMxQjYxdJ32DKhuiYNGbwnEbEg\
vMBt0C3nid9Fe'
MQTT_PASS = 'bEEvvyn1bxDFw0-s'
    
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK: returned code: ", rc)
        result = client.subscribe("alarm", qos=1)
        print("subscription result: ", result)
    else:
        print("Bad connection Returned code: ", rc)

def on_message(client, userdata, message):
    print("message payload: ", message.payload)
    # datetime object containing current date and time
    now = datetime.now()
    print( "current time: ", now.strftime("%d/%m/%Y %H:%M:%S") )

client = mqtt.Client("alarm_notification_receiver_emulator.py", userdata={})
ssl_context= ssl_alpn()
client.tls_set_context(context=ssl_context) 
client.on_connect = on_connect
client.on_message = on_message
print("connecting to broker...")
client.connect(aws_iot_endpoint, port=443)
client.loop_forever()

