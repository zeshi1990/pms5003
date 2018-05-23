import time
from pms5003_driver import PMS5003
from awsiotconn import MQTTCONN

def main():
    sensor = PMS5003(port="/dev/ttyO1", baudrate=9600)
    sensor.initialize()

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
        data = sensor.read_passive()
        print data
        time.sleep(2)

if __name__ == "__main__":
    main()
