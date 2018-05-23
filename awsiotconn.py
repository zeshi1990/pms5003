#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform

class MQTTCONN:

    def __init__(self, awshost, awsport, topic, caPath, certPath, keyPath, listener=False):
        self.topic = topic
        self.connect = False
        self.listener = listener
        self._mqttc = paho.Client()
        self._mqttc.on_connect = self.__on_connect
        self._mqttc.on_message = self.__on_message
        self._mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self._mqttc.connect(awshost, awsport, keepalive=300)
        if not listener:
            self._mqttc.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        self.connect = True
        print("Conncetion returned result: " + str(rc))
        if self.listener:
            self._mqttc.subscribe(self.topic, qos=1)

    def __on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def publish(self, topic, payload):
        sleep(0.5)
        if self.connect:
            print("sending data {}".format(payload))
            self._mqttc.publish(topic, payload, qos=1)

    def subscribe(self):
        if self.connect:
            self._mqttc.loop_forever()


def main():
    awshost = "data.iot.us-east-2.amazonaws.com"
    awsport = 8883
    clientId = "pm25Sensor"
    topic = "pm25"
    thingName = "pm25Sensor"
    caPath = "cert/aws-iot-rootCA.crt"
    certPath = "cert/cert.pem"
    keyPath = "cert/privkey.pem"

    mqttconn = MQTTCONN(awshost, awsport, topic, caPath, certPath, keyPath, listener=False)
    while True:
        mqttconn.publish(topic, 10)

if __name__ == "__main__":
   main()
