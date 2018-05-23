from influxdb import InfluxDBClient
from datetime import datetime

class INFLUXCONN:
    def __init__(self, host="localhost", port="8086", user="root", passwd="root", db="home", table="home_air"):
        self.client = InfluxDBClient(host, port, user, passwd, db)
        self.client.create_database(db)
        self.table = table

    def write_data(self, payload):
        payload_list = payload.split(",")
        len_vals = len(payload_list) / 2
        dt_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%HZ")
        for i in range(len_vals):
            dtype = payload_list[i*2].strip()
            val = float(payload_list[i*2+1].strip())
            json_body = {
                "measurement": self.table,
                "tags": {
                    "type": dtype
                },
                "time": dt_string,
                "fields": {
                    "value": val
                }
            }
            self.client.write_points(json_body)
