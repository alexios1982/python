import base64
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import ssl

IoT_protocol_name = "x-amzn-mqtt-ca"

aws_iot_endpoint = "a2x7fkplgngdk8-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
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

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK: returned code: ", rc)
        #result = client.subscribe("Notifications", qos=1)
        result = client.subscribe("alarm", qos=1)
        print("subscription result: ", result)
    else:
        print("Bad connection Returned code: ", rc)

def on_message(client, userdata, message):
    print("message payload: ", message.payload)
    now = datetime.now()
    print( "current time: ", now.strftime("%d/%m/%Y %H:%M:%S") )

if __name__ == '__main__':
    topic = "Notifications"
    try:
        mqttc = mqtt.Client("alarm_notification_receiver_emulator")
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
