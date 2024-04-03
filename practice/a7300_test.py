from os import error
from urllib import response
from pymodbus.client import ModbusTcpClient as ModbusClient
import time
import os, glob
from datetime import datetime

from ocrsettingtest import Ocrsetting
    
class SetupTesting:
    
    SERVER_IP = '10.10.26.159'  # 장치 IP 주소
    SERVER_PORT = 5100  #A7300

    image_path = r"\\10.10.20.30\screenshot"

    search_pattern = os.path.join(image_path, './**/*10.10.26.159*.png')
    now = datetime.now()
    file_time_diff = {}

    def __init__(self):
        self.A7300client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT)
        self.connection = self.A7300client.connect()

    def tcp_connect(self):
        self.A7300client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT)
        connection = self.A7300client.connect()
        if connection:
            print("Success")
        else:
            print("Fail")
            
    def tcp_disconnect(self):
        if self.A7300client:
            self.A7300client.close()
            print("Disconnect")
        else:
            error()

    def setup_all_test(self):
        if self.connection:
            print("Success")
        else:
            print("Fail")
        self.address = 57100
        self.value = 1

        hex_string = "A5A5"
        self.bytes_data = bytes.fromhex(hex_string)

        self.address1 = 57101
        if self.A7300client:
            # self.response = self.client.write_register(self.address, self.value)
            # time.sleep(1)
            hex_value = int(hex_string, 16)
            self.response = self.A7300client.write_register(self.address1, hex_value)
            print(self.response)
            print("good")
        else:
            print(self.response.isError())

    def moving_cursor(self):
        for _ in range(2):
            if self.A7300client:
                self.address = 57110
                self.value = 100
                self.response = self.A7300client.write_register(self.address, self.value)
                time.sleep(1)
                self.address1 = 57111
                self.value1 = 130
                self.response1 = self.A7300client.write_register(self.address1, self.value1)
                time.sleep(1)
                self.address2 = 57112
                self.value2 = 1
                self.value3 = 0
                self.response2 = self.A7300client.write_register(self.address2, self.value2)
                time.sleep(1)
                self.response3 = self.A7300client.write_register(self.address2, self.value3)
                #65, 180
            else:
                print(self.response3.isError())


    def load_image_file(self):
        for file_path in glob.glob(self.search_pattern, recursive=True):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            time_diff = abs((self.now - creation_time).total_seconds())
            self.file_time_diff[file_path] = time_diff

        closest_file = min(self.file_time_diff, key=self.file_time_diff.get, default=None)
        normalized_path = os.path.normpath(closest_file)

        print("가장 가까운 시간에 생성된 파일:", normalized_path)

        return normalized_path




test123 = SetupTesting()
ocr = Ocrsetting()
test123.moving_cursor()
time.sleep(2)
test123.setup_all_test()
path123 = test123.load_image_file()
ocr.meas_vol_test(path123)

test123.tcp_disconnect()