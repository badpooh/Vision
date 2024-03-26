from http import client
from os import error
from urllib import response
from pymodbus.client import ModbusTcpClient as ModbusClient


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
        self.client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT)
        if self.client:
            self.client.close()
            print("Disconnect")
        else:
            error()

    def setup_all_test(self):
        self.address = 57100
        self.address1 = 57101
        self.value = 1
        self.value1 = 23130
        if self.client:
            self.response = self.client.write_register(self.address, self.value)
            self.answer = self.client.read_holding_registers(self.address, 1)
            self.response1 = self.client.write_register(self.address1, self.value1)
            print(self.answer)
        else:
            print(self.response.isError())

test = SetupTesting()
# test.tcp_connect()
# test.setup_all_test()
test.tcp_disconnect()