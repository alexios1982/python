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

def decode_payload(encoded_payload, client):
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
    print("retrieving information from payload")
    ring = json_payload["ring"]
    muuid = json_payload["muuid"]
    print("mmuid: ", muuid)
    print("Received ring and muuid")
    # Get data and decode the binary content
    bytes_json_payload = bytes(json_payload["media"], 'utf-8')
    print("Received media to decode")
    image_64_decode = base64.decodebytes(bytes_json_payload)
    with open("prova.jpg", 'wb') as f:
        f.write(image_64_decode)
    print("file decoded")
    ##################################################################
    #create a response
    #json format
    json_response = {"ring" : ring, "muuid" : muuid, "owner" : 0, "monitored" : 0, "unknown" : 1}
    #let's convert to string
    payload = json.dumps(json_response)
    client.publish("User_Consitalia_1_aws/Response", payload, qos = 1)
    print("reponse sent")    

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK: returned code: ", rc)
        result = client.subscribe("User_Consitalia_1_aws/Notifications", qos=2)
        print("subscription result: ", result)
    else:
        print("Bad connection Returned code: ", rc)

def on_message(client, userdata, message):
    #print("message topic: ", message.topic)
    # datetime object containing current date and time
    now = datetime.now()
    print( "current time: ", now.strftime("%d/%m/%Y %H:%M:%S") )
    decode_payload(message.payload, client)

client = mqtt.Client("ai_server_emulator.py", userdata={})
client.tls_set() 
client.username_pw_set(MQTT_TOKEN_FLESPI, MQTT_PASS)  
client.on_connect = on_connect
client.on_message = on_message
print("connecting to broker...")
client.connect(MQTT_SERVER_FLESPI, 8883, 60)
client.loop_forever()

