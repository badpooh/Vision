from http import client
from os import error
from urllib import response
from pymodbus.client import ModbusTcpClient as ModbusClient
import time
    
class SetupTesting:
    
    SERVER_IP = '10.10.26.159'  # 장치 IP 주소
    SERVER_PORT = 5100  #A7300

    def tcp_connect(self):
        self.client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT)
        connection = self.client.connect()
        if connection:
            print("Success")
        else:
            print("Fail")
            
    def tcp_disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnect")
        else:
            error()

    def setup_all_test(self):
        self.client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT)
        connection = self.client.connect()
        if connection:
            print("Success")
        else:
            print("Fail")
        self.address = 57100
        self.value = 1

        hex_string = "A5A5"
        self.bytes_data = bytes.fromhex(hex_string)

        self.address1 = 57101
        if self.client:
            # self.response = self.client.write_register(self.address, self.value)
            # time.sleep(1)
            hex_value = int(hex_string, 16)
            self.response = self.client.write_register(self.address1, hex_value)
            print(self.response)
            print("good")
        else:
            print(self.response.isError())

    def moving_cursor(self):
        self.client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT)
        connection = self.client.connect()
        if connection:
            self.address = 57110
            self.value = 65
            self.address1 = 57111
            self.value1 = 180
            self.address2 = 57112
            self.value2 = 1
            #65, 180
            pass





test123 = SetupTesting()
test123.setup_all_test()
test123.tcp_disconnect()