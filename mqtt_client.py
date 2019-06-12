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

def decode_payload(encoded_payload):
    """!
    @brief This method encapsulates the decoding procedures needed to get
    the video chunk and save it to the RAM disk.
    The original message is encoded in json format, and its 'data' field is
    further encoded in base64 and converted to utf-8 string. This method
    performs the inverse operations to get the decoded video in binary
    format, then write it to disk and returns the url.
    @param encoded_payload: The content of the MQTTMessage payload.
    """
    # Decode json
    json_payload = json.loads(encoded_payload)
    filename = json_payload["filename"]
    print("Received file: ", filename)
    # Get data and decode the binary content
    bytes_json_payload = bytes(json_payload["data"], 'utf-8')
    image_64_decode = base64.decodebytes(bytes_json_payload)
    with open(filename, 'wb') as f:
        f.write(image_64_decode)
        
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK: returned code: ", rc)
        result = client.subscribe("User_Consitalia_1/Notifications", qos=2)
        print("subscription result: ", result)
    else:
        print("Bad connection Returned code: ", rc)

def on_message(client, userdata, message):
    #print("message topic: ", message.topic)
    # datetime object containing current date and time
    now = datetime.now()
    print( "current time: ", now.strftime("%d/%m/%Y %H:%M:%S") )
    decode_payload(message.payload)

client = mqtt.Client("python-client", userdata={})
client.tls_set() 
client.username_pw_set(MQTT_TOKEN_FLESPI, MQTT_PASS)  
client.on_connect = on_connect
client.on_message = on_message
print("connecting to broker...")
client.connect(MQTT_SERVER_FLESPI, 8883, 60)
client.loop_forever()

