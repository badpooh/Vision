from os import error
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import time
import os, glob
from datetime import datetime

class ModbusManager:
    
    SERVER_IP = '10.10.26.159'  # 장치 IP 주소
    TOUCH_PORT = 5100  #내부터치
    SETUP_PORT = 502  #설정
    
    def __init__(self):
        self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
        self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)
        
    def tcp_connect(self):
        if not self.touch_client.connect():
            print("Failed to connect touch client")
        if not self.setup_client.connect():
            print("Failed to connect setup client")
            
    def check_connection(self):
        while True:
            if not self.touch_client.is_socket_open():
                print("Touch client disconnected, reconnecting...")
                self.touch_client.connect()
            if not self.setup_client.is_socket_open():
                print("Setup client disconnected, reconnecting...")
                self.setup_client.connect()
            time.sleep(1)
    
    def start_monitoring(self):
        threading.Thread(target=self.check_connection, daemon=True).start()
        
class TouchManager:
    
    def measurement_touch(self):
        pass

    def event_touch(self):
        pass

    def network_touch(self):
        pass
    
    def control_touch(self):
        pass
        
    def system_touch(self):
        pass
    

    
    
class SetupTesting:
    
    SERVER_IP = '10.10.26.159'  # 장치 IP 주소
    TOUCH_PORT = 5100  #A7300 - 터치용
    SETUP_PORT = 502  #A7300 - 설정용

    image_path = r"\\10.10.20.30\screenshot"

    search_pattern = os.path.join(image_path, './**/*10.10.26.159*.png')
    now = datetime.now()
    file_time_diff = {}

    def __init__(self):
        self.A7300client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT1)
        self.connection = self.A7300client.connect()
        self.A7300client.write_register(2900, 2300)
        self.A7300client.write_register(2900, 0)
        self.A7300client.write_register(2900, 700)
        self.A7300client.write_register(2900, 1)
        self.A7300client.read_holding_registers(2900, 1)
        self.A7300client.write_register(2901, 2300)
        self.A7300client.write_register(2901, 0)
        self.A7300client.write_register(2901, 1600)
        self.A7300client.write_register(2901, 1)
        self.A7300client.read_holding_registers(2901, 1)

    def tcp_connect(self):
        self.A7300client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
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

    def change_wiring(self):
            if self.A7300client:
                
                # print(self.readRes)
                # self.address1 = 2901
                # self.value4 = 2300
                # self.value5 = 1
                # self.value6 = 1600
                # self.value7 = 1
                # self.response4 = self.A7300client.write_register(self.address1, self.value4)
                # self.response5 = self.A7300client.write_register(self.address1, self.value5)
                # self.response6 = self.A7300client.write_register(self.address1, self.value6)
                # self.response7 = self.A7300client.write_register(self.address1, self.value7)
                time.sleep(1)
                self.response8 = self.A7300client.write_register(6001, 1)
                time.sleep(1)
                self.response9 = self.A7300client.write_register(6000, 1)
                time.sleep(1)
                self.response10 = self.A7300client.read_holding_registers(6000, 1)
                
            else:
                print(self.response10.isError())


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
# ocr = Ocrsetting()
# test123.moving_cursor()
# time.sleep(2)
# test123.setup_all_test()
# path123 = test123.load_image_file()
# ocr.meas_vol_test(path123)

# test123.tcp_disconnect()
test123.change_wiring()
test123.tcp_disconnect()

