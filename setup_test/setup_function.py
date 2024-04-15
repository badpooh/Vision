from os import error
import threading
import time
import numpy as np
import os, glob
from itertools import chain
import cv2
import easyocr
from datetime import datetime
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading

from setup_test.setup_config import ConfigSetup

config_data = ConfigSetup()

class ModbusManager:
    
    SERVER_IP = '10.10.26.156'  # 장치 IP 주소
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
        
class TouchManager:
    
    mobus_manager = ModbusManager()
    measurement, mea_voltage = config_data.color_detection_data()
    main_menu_1, side_menu_1, data_view_1 = config_data.touch_data()
    ui_test_mode, screen_capture, pos_x, pos_y, touch_mode = config_data.touch_address_data()
    hex_value = int("A5A5", 16)
    
    def __init__(self):
        self.client_check = self.mobus_manager.touch_client
        
    def touch_write(self, address, value, delay=0.6):
        self.client_check.write_register(address, value)
        time.sleep(delay)
    
    def data_view_touch(self):
        ############ Wiring에서 3P4W -> 3P3W로 변경완료 ###############
        if self.client_check:
            self.touch_write(self.ui_test_mode, 1)
            for _ in range(2):
                self.touch_write(self.pos_x, self.main_menu_1[0])
                self.touch_write(self.pos_y, self.main_menu_1[1])
                self.touch_write(self.touch_mode, 1)
                self.touch_write(self.touch_mode, 0)
            self.touch_write(self.screen_capture, self.hex_value)
            self.touch_write(self.pos_x, self.data_view_1[0])
            self.touch_write(self.pos_y, self.data_view_1[1])
            self.touch_write(self.touch_mode, 1)
            self.touch_write(self.touch_mode, 0)
            self.touch_write(self.pos_x, 400)
            self.touch_write(self.pos_y, 160)
            self.touch_write(self.touch_mode, 1)
            self.touch_write(self.touch_mode, 0)
            self.touch_write(self.pos_x, 340)
            self.touch_write(self.pos_y, 430)
            self.touch_write(self.touch_mode, 1)
            self.touch_write(self.touch_mode, 0)
            self.touch_write(self.pos_x, 620)
            self.touch_write(self.pos_y, 150)
            self.touch_write(self.touch_mode, 1)
            self.touch_write(self.touch_mode, 0)
            self.touch_write(self.screen_capture, self.hex_value)
            ########### 완료 후 스크린샷 까지 ###################
        else:
            print("client Error")




        pass

    def event_touch(self):
        pass

    def network_touch(self):
        pass
    
    def control_touch(self):
        pass
        
    def system_touch(self):
        pass
    
class EditImage:
    
    rois = config_data.roi()
    
    ########################## 이미지 커팅 기본 method ##########################
    def image_cut(self, image, height_ratio_start, height_ratio_end, width_ratio_start, width_ratio_end):
        height, width = image.shape[:2]
        cropped_image = image[int(height*height_ratio_start):int(height*height_ratio_end),
                            int(width*width_ratio_start):int(width*width_ratio_end)]
        resized_image = cv2.resize(cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # 이미지 블러 처리 및 선명하게 만들기
        blurred_image = cv2.GaussianBlur(resized_image, (0, 0), 3)
        sharpened_image = cv2.addWeighted(resized_image, 1.5, blurred_image, -0.5, 0)
        return sharpened_image
    ####################################################
    
    def image_cut_custom(self, image):
        image = cv2.imread(image)
        resized_image = cv2.resize(image, None, None, 3, 3, cv2.INTER_CUBIC)
        blurred_image = cv2.GaussianBlur(resized_image, (0, 0), 3)
        sharpened_image = cv2.addWeighted(resized_image, 1.5, blurred_image, -0.5, 0)

        reader = easyocr.Reader(['en'])

        # 각 ROI에 대해 OCR 처리 및 결과 수집
        ocr_results = {}
        for roi_key, (x, y, w, h) in self.rois.items():
            roi_image = sharpened_image[y:y+h, x:x+w]
            cv2.imshow('Image with Size Info', roi_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            text_results = reader.readtext(roi_image, paragraph=False)  # 해당 ROI에 대해 OCR 수행

            # 추출된 텍스트 합치기
            extracted_texts = ' '.join([text[1] for text in text_results])

            ocr_results[roi_key] = extracted_texts

        # OCR 결과 출력
        for roi_key, text in ocr_results.items():
            print(f'ROI {roi_key}: {text}')

        return ocr_results

class UiTest:

    answer_voltage, answer_voltage = config_data.roi_answers()

    def measurement_voltage_uitest(self, ocr_results_1):

            ocr_right_1 = self.answer_voltage

            right_set_1 = set(text.strip() for text in ocr_right_1)

            ocr_set_1 = set(result.strip() for result in ocr_results_1)


            leave_ocr_all = [
            (ocr_set_1 - right_set_1),
            ]
            leave_right_all = [
                (right_set_1 - ocr_set_1),
            ]
            
            ocr_error = list(chain(*leave_ocr_all))
            right_error = list(chain(*leave_right_all))

            # OCR 결과와 매칭되지 않아 남은 단어
            print(f"OCR 결과와 매칭되지 않는 단어들: {ocr_error}")
            print(f"\n정답 중 OCR 결과와 매칭되지 않는 단어들: {right_error}")
            
            # cv2.imshow('Image with Size Info', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            return ocr_error, right_error    
    
# class SetupTesting:
    
#     SERVER_IP = '10.10.26.159'  # 장치 IP 주소
#     TOUCH_PORT = 5100  #A7300 - 터치용
#     SETUP_PORT = 502  #A7300 - 설정용

#     image_path = r"\\10.10.20.30\screenshot"

#     search_pattern = os.path.join(image_path, './**/*10.10.26.159*.png')
#     now = datetime.now()
#     file_time_diff = {}

#     def __init__(self):
#         self.A7300client = ModbusClient(self.SERVER_IP, port=self.SERVER_PORT1)
#         self.connection = self.A7300client.connect()
#         self.A7300client.write_register(2900, 2300)
#         self.A7300client.write_register(2900, 0)
#         self.A7300client.write_register(2900, 700)
#         self.A7300client.write_register(2900, 1)
#         self.A7300client.read_holding_registers(2900, 1)
#         self.A7300client.write_register(2901, 2300)
#         self.A7300client.write_register(2901, 0)
#         self.A7300client.write_register(2901, 1600)
#         self.A7300client.write_register(2901, 1)
#         self.A7300client.read_holding_registers(2901, 1)

#     def setup_all_test(self):
#         if self.connection:
#             print("Success")
#         else:
#             print("Fail")
#         self.address = 57100
#         self.value = 1

#         hex_string = "A5A5"
#         self.bytes_data = bytes.fromhex(hex_string)

#         self.address1 = 57101
#         if self.A7300client:
#             # self.response = self.client.write_register(self.address, self.value)
#             # time.sleep(1)
#             hex_value = int(hex_string, 16)
#             self.response = self.A7300client.write_register(self.address1, hex_value)
#             print(self.response)
#             print("good")
#         else:
#             print(self.response.isError())

#     def moving_cursor(self):
#         for _ in range(2):
#             if self.A7300client:
#                 self.address = 57110
#                 self.value = 100
#                 self.response = self.A7300client.write_register(self.address, self.value)
#                 time.sleep(1)
#                 self.address1 = 57111
#                 self.value1 = 130
#                 self.response1 = self.A7300client.write_register(self.address1, self.value1)
#                 time.sleep(1)
#                 self.address2 = 57112
#                 self.value2 = 1
#                 self.value3 = 0
#                 self.response2 = self.A7300client.write_register(self.address2, self.value2)
#                 time.sleep(1)
#                 self.response3 = self.A7300client.write_register(self.address2, self.value3)
#                 #65, 180
#             else:
#                 print(self.response3.isError())

#     def change_wiring(self):
#             if self.A7300client:
                
#                 # print(self.readRes)
#                 # self.address1 = 2901
#                 # self.value4 = 2300
#                 # self.value5 = 1
#                 # self.value6 = 1600
#                 # self.value7 = 1
#                 # self.response4 = self.A7300client.write_register(self.address1, self.value4)
#                 # self.response5 = self.A7300client.write_register(self.address1, self.value5)
#                 # self.response6 = self.A7300client.write_register(self.address1, self.value6)
#                 # self.response7 = self.A7300client.write_register(self.address1, self.value7)
#                 time.sleep(1)
#                 self.response8 = self.A7300client.write_register(6001, 1)
#                 time.sleep(1)
#                 self.response9 = self.A7300client.write_register(6000, 1)
#                 time.sleep(1)
#                 self.response10 = self.A7300client.read_holding_registers(6000, 1)
                
#             else:
#                 print(self.response10.isError())


#     def load_image_file(self):
#         for file_path in glob.glob(self.search_pattern, recursive=True):
#             creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
#             time_diff = abs((self.now - creation_time).total_seconds())
#             self.file_time_diff[file_path] = time_diff

#         closest_file = min(self.file_time_diff, key=self.file_time_diff.get, default=None)
#         normalized_path = os.path.normpath(closest_file)

#         print("가장 가까운 시간에 생성된 파일:", normalized_path)

#         return normalized_path




# test123 = SetupTesting()
# # ocr = Ocrsetting()
# # test123.moving_cursor()
# # time.sleep(2)
# # test123.setup_all_test()
# # path123 = test123.load_image_file()
# # ocr.meas_vol_test(path123)

# # test123.tcp_disconnect()
# test123.change_wiring()
# test123.tcp_disconnect()

