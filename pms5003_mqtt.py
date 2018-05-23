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
        pm25 = data["pm25"]
        pm10 = data["pm10"]
        pm100 = data["pm100"]
        payload = "pm25, {0}, pm10, {1}, pm100, {2}".format(pm25, pm10, pm100)
        mqttconn.publish("home_air_quality", payload)
        sensor.set_mode("sleep")
        time.sleep(10)
        sensor.set_mode("wakeup")
        time.sleep(10)


if __name__ == "__main__":
    main()
