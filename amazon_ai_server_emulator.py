import base64
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import ssl

# MQTT_SERVER_FLESPI = 'mqtt.flespi.io'
# MQTT_TOKEN_FLESPI = 'FlespiToken ' \
#                     'R4XF03Rp3KStynVTDRrOuju7odMxQjYxdJ32DKhuiYNGbwnEbEg\
# vMBt0C3nid9Fe'
# MQTT_PASS = 'bEEvvyn1bxDFw0-s'

IoT_protocol_name = "x-amzn-mqtt-ca"
#aws_iot_endpoint = "AWS_IoT_ENDPOINT_HERE" # <random>.iot.<region>.amazonaws.com
aws_iot_endpoint = "a2x7fkplgngdk8-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
#aws_iot_endpoint = "a2x7fkplgngdk8-ats.iot.eu-central-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

ca = "./AmazonRootCA1.pem" 
cert = "./33ac0ac8dc-certificate.pem.crt"
private = "./33ac0ac8dc-private.pem.key"

def ssl_alpn():
    try:
        #debug print opnessl version
        print("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

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
    with open( muuid + ".jpg", 'wb') as f:
        f.write(image_64_decode)
    print("file decoded")
    ##################################################################
    #create a response
    #json format
    json_response = {"ring" : ring, "muuid" : muuid, "owner" : 0, "monitored" : 0, "unknown" : 1}
    #let's convert to string
    payload = json.dumps(json_response)
    client.publish("ai_reply", payload, qos = 1)
    print("reponse sent")    

        
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK: returned code: ", rc)
        #result = client.subscribe("Notifications", qos=1)
        result = client.subscribe("ai_request", qos=1)
        print("subscription result: ", result)
    else:
        print("Bad connection Returned code: ", rc)

def on_message(client, userdata, message):
    #print("message topic: ", message.topic)
    # datetime object containing current date and time
    now = datetime.now()
    print( "current time: ", now.strftime("%d/%m/%Y %H:%M:%S") )
    decode_payload(message.payload, client)

# client = mqtt.Client("python-client", userdata={})
# client.tls_set() 
# client.username_pw_set(MQTT_TOKEN_FLESPI, MQTT_PASS)  
# client.on_connect = on_connect
# client.on_message = on_message
# print("connecting to broker...")
# client.connect(MQTT_SERVER_FLESPI, 8883, 60)
# client.loop_forever()

if __name__ == '__main__':
    topic = "Notifications"
    try:
        mqttc = mqtt.Client("python-client")
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        print("start connect")
        mqttc.connect(aws_iot_endpoint, port=443)
        print("connect success")
        #mqttc.loop_start()

        # while True:
        #     now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        #     print("try to publish:{}".format(now))
        #     out = mqttc.publish(topic, now)
        #     time.sleep(1)
        print ("starting the loop")
        mqttc.loop_forever()

    except Exception as e:
        print("exception main()")
        print("e obj:{}".format(vars(e)))
        print("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
