import Adafruit_BBIO.UART as UART
UART.setup("UART1")
import serial
import datetime
import struct
import time


class PMS5003(serial.Serial):
    def initialize(self):
        self.set_mode('passive')

    def read_passive(self):
        cmd = self.format_cmd("read")
        self.write(cmd)
        print "start parsing results"
        res_data = self.parse_data()
        if res_data is None:
            print "Read passive failed"
            return None
        else:
            res = self.format_data(res_data)
            return res

    @staticmethod
    def format_data(rcv):
        fields = ["apm10", "apm25", 'apm100',
                  'pm10', 'pm25', 'pm100',
                  'gt03um', 'gt05um', 'gt10um',
                  'gt25um', 'gt50um', 'gt100um']
        res = {
            'timestamp': datetime.datetime.now(),
        }
        for i, f in enumerate(fields):
            idx_1 = i * 2 + 4
            idx_2 = i * 2 + 5
            res[f] = ord(rcv[idx_1]) * 256 + ord(rcv[idx_2])
        return res

    def parse_data(self):
        rv = b''
        ch1 = self.read()
        if ch1 == b'\x42':
            ch2 = self.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += self.read(28)
                self.read(2)
                return rv
        return None

    def set_mode(self, mode):
        assert mode in ["passive", "active", "sleep", "wakeup"]
        mode_cmd = self.format_cmd(mode)
        cmd_return = self.get_cmd_correct_return(mode)
        if mode != "wakeup":
            sum_cmd_return = sum(cmd_return)
        self.write(mode_cmd)
        if mode == "wakeup":
            return 0
        ss = self.read(8)
        res = sum([ord(c) for c in ss])
        print mode, res, sum_cmd_return
        if res == sum_cmd_return:
            print "The {} mode is set!".format(mode)
        else:
            print "The {} mode set failed!".format(mode)
            self.set_mode(mode)
        return 0

    @staticmethod
    def get_cmd_correct_return(mode='passive'):
        if mode == "wakeup":
            return 0
        e = None
        no = None
        chckSum = 0x42 + 0x4D + 0x00 + 0x04
        if mode == "passive":
            e = 0xE1
            no = 0x0
        elif mode == "active":
            e = 0xE1
            no = 0x01
        elif mode == "sleep":
            e = 0xE4
            no = 0x0
        chckSum += e + no
        res = struct.pack("!BBBBBBH", 0x42, 0x4D, 0x00, 0x04, e, no, chckSum)
        res = struct.unpack("!BBBBBBBB", res)
        return res

    def format_cmd(self, mode='passive'):
        cmd = None
        ON = None
        chckSum = 0x42 + 0x4D
        if mode == "passive":
            cmd = 0xE1
            ON = 0x0
        elif mode == "active":
            cmd = 0xE1
            ON = 0x1
        elif mode == "read":
            cmd = 0xE2
            ON = 0x0
        elif mode == "sleep":
            cmd = 0xE4
            ON = 0x0
        elif mode == "wakeup":
            cmd = 0xE4
            ON = 0x01
        chckSum += cmd + 0x00 + ON
        data = struct.pack('!BBBBBH', 0x42, 0x4D, cmd, 0x0, ON, chckSum)
        cmd = struct.unpack("!BBBBBBB", data)
        return cmd


def main():
    sensor = PMS5003(port="/dev/ttyO1", baudrate=9600)
    sensor.initialize()
    time.sleep(2)
    print "Start reading passive"
    while True:
        data = sensor.read_passive()
        print data
        time.sleep(2)
        sensor.set_mode("sleep")
        time.sleep(2)
        sensor.set_mode("wakeup")
        time.sleep(2)


if __name__ == "__main__":
    main()
