import serial
import time
import logging
import json
import os

logger = logging.getLogger(__name__)


class connector:
    def __init__(self, path_to_prefernces=None):
        self.tunnel = self.create_com_port(path_to_prefernces)

        # self.tunnel.baudrate = 115200
        # self.tunnel.port = 'COM3'
        # self.tunnel.timeout = 0.5
        # self.tunnel.write_timeout = 0.5

        if not self.tunnel.is_open:
            self.tunnel.open()
        logger.info("Connector to COM port was successful created")

    def get_com_port(self):
        return self.tunnel

    def create_com_port(self, path_to_preferences=None) -> object:
        data = self.read_comport_preferences(path_to_preferences)
        if data is None:
            return serial.Serial(
                port='COM3',
                baudrate=9600,
                timeout=0.5,
                writeTimeout=0.5
            )
        else:
            return serial.Serial(
                port=data['port'],
                baudrate=data['baudrate'],
                timeout=data['timeout'],
                write_timeout=data['write_timeout'],
            )

    def read_comport_preferences(self, path: object) -> object:
        """ get com port preferences
        :type path: object
        :param path: #path to com port json file preferences
        :return object: {'port':' 'baudrate':' "parity":' "stopbits":' "bytesize":}
        :Date: 2022-11-27
        :Version: 1
        :Authors: bodomus@gmail.com
        """
        if not os.path.isfile(path):
            raise Exception("invalid file path {!r}".format(path))
        logger.info("read port prefernces from file %s", path)
        with open(path) as json_file:
            data = json.load(json_file)
            return {'port': data['port'], 'baudrate': data['baudrate'], "parity": data['parity'],
                    "write_timeout": data['write_timeout'], "bytesize": data['bytesize'], "timeout": data['timeout']}

# with serial.Serial() as ser:
#     ser.baudrate = 115200
#     ser.port = 'COM3'
#     ser.timeout = 0.5
#     ser.write_timeout = 0.5
#     # ser.rtscts = True
#     ser.open()
#     # time.sleep(2)
#     l = [118, 0, 8, 37, 0, 0, 0, 2, 0, 10, 13]
#     # m = [31, 31, 38, 20, 30, 20, 38, 20, 33, 37, 20, 30, 20, 30, 20, 30, 20, 32, 20, 30]
#
#     while 1:
#         if not ser.is_open:
#             ser.open()
#         time.sleep(1)
#         len = ser.write(l)
#         print(f'Send {len} bytes')
#         # ser.flush()
#
#         r = ser.read(4)
#         # print(f'R={r} length: {len(r)}')
#         # ser.read_until(size=10)
#         while ser.in_waiting:
#             data = ser.readline().decode("ascii")
#             print(f'Data={data} length: {len(data)}')
#
#         ser.close()
#         if not ser.is_open:
#             print('port close')
