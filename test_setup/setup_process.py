import cv2
import easyocr
import numpy as np
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading


path123 = r".\image_test\a7300_mea_voltage.png"


class ModbusManager:
    
    SERVER_IP = '10.10.26.159'  # 장치 IP 주소
    TOUCH_PORT = 5100  #내부터치
    SETUP_PORT = 502  #설정
    
    def __init__(self):
        self.is_connected = False 
        self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
        self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)
        
    def tcp_connect(self):
        if self.touch_client.connect() and self.setup_client.connect():
            self.is_connected = True
            print("is connected")
        if not self.touch_client.connect():
            print("Failed to connect touch client")
        if not self.setup_client.connect():
            print("Failed to connect setup client")
            
    def check_connection(self):
        while self.is_connected:
            if not self.touch_client.is_socket_open():
                print("Touch client disconnected, reconnecting...")
                if self.touch_client.connect():
                    print("touch_client connected")
            if not self.setup_client.is_socket_open():
                print("Setup client disconnected, reconnecting...")
                if self.setup_client.connect():
                    print("setup_client connected")
            time.sleep(1)
    
    def start_monitoring(self):
        self.tcp_connect()
        threading.Thread(target=self.check_connection, daemon=True).start()

    def tcp_disconnect(self):
        self.touch_client.close()
        self.setup_client.close()
        self.is_connected = False
        print("is disconnected")


class SetupProcess:

    mobus_manager = ModbusManager()

    def __init__(self):
        self.client_check = self.mobus_manager.touch_client
    
    def measurement_test(self):
        if self.client_check:
            self.client_check.write_register(57100, 1)
            time.sleep(0.6)
            for _ in range(2):
                self.client_check.write_register(57110, 100)
                time.sleep(0.6)
                self.client_check.write_register(57111, 85)
                time.sleep(0.6)
                self.client_check.write_register(57112, 1)
                time.sleep(0.6)
                self.client_check.write_register(57112, 0)
                time.sleep(0.6)
            self.hex_value = int("A5A5", 16)
            self.client_check.write_register(57101, self.hex_value)

        else:
            print("client Error")


    
    
#     # 색 감 비교 코드
#     # def meas_vol_test(self, path123):
#     #     image = cv2.imread(path123)

#     #     def color_detection(a, b, c, d, R, G, B):
#     #         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     #         x, y, w, h = a, b, c, d 
#     #         selected_area = image_rgb[y:y+h, x:x+w]
#     #         average_color = np.mean(selected_area, axis=(0, 1))
#     #         target_color = np.array([R, G, B])
#     #         color_difference = np.linalg.norm(average_color - target_color)
#     #         return color_difference

#     #     color_result1 = color_detection(*measurement)
#     #     color_result2 = color_detection(*mea_voltage)
        
#     #     print(color_result1)
#     #     print(color_result2)

#         # if color_result1 < 5 and color_result2 < 5:
#         #     cut_voltage_image = self.cut_image(image, 0.25, 1, 0.2, 1)
#         #     ocr_error, right_error = self.measurement_voltage_uitest(cut_voltage_image)
#         #     if not ocr_error and not right_error:
#         #         print("pass")
#         #     else:
#         #         print("Fail")
#         # else:
#         #     print("fail")
            
#     def meas_cur_test(self):
#         #숫자 0 인식이 안됨 개선 필요
#         image = cv2.imread(path123)

#         def color_detection(a, b, c, d, R, G, B):
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             x, y, w, h = a, b, c, d 
#             selected_area = image_rgb[y:y+h, x:x+w]
#             average_color = np.mean(selected_area, axis=(0, 1))
#             target_color = np.array([R, G, B])
#             color_difference = np.linalg.norm(average_color - target_color)
#             return color_difference

#         color_result1 = color_detection(5, 70, 10, 10, 47, 180, 139)
#         color_result2 = color_detection(110, 170, 10, 10, 255, 255, 255)

#         if color_result1 < 5 and color_result2 < 5:
#             cut_current_image = self.cut_image(image, 0.25, 1, 0.2, 1)
#             ocr_error, right_error = self.measurement_currnet_uitest(cut_current_image)
#             if not ocr_error and not right_error:
#                 print("pass")
#             else:
#                 print("Fail")
#         else:
#             print("fail")
            
            
# test002 = SetupProcess()
# tt = test002.meas_vol_test(path123)