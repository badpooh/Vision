from os import error
import threading
import time
import numpy as np
import re
from itertools import chain
import cv2
import easyocr
from datetime import datetime
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import torch

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
    hex_value = int("A5A5", 16)
    
    def __init__(self):
        self.client_check = self.mobus_manager.touch_client
        self.coords_touch = config_data.touch_data()
        self.coords_color = config_data.color_detection_data()
        self.coords_TA = config_data.touch_address_data()
        
    def touch_write(self, address, value, delay=0.6):
        attempt = 0
        while attempt < 2:
            self.client_check.write_register(address, value)
            read_value = self.client_check.read_holding_registers(address)
            time.sleep(delay)
            
            if read_value == value:
                return
            else:
                attempt += 1
        print(f"Failed to write value {value} to address {address}. Read back {read_value} instead.")
        
        
    def uitest_mode_start(self):
        if self.client_check:
            self.touch_write(self.coords_TA["ui_test_mode"], 1)
        else:
            print("client Error")
            
    def screenshot(self):
        if self.client_check:
            self.touch_write(self.coords_TA["screen_capture"], self.hex_value)
        else:
            print("client Error")

    def menu_touch(self, menu_key):
        if self.client_check:
            data_view_x, data_view_y = self.coords_touch[menu_key]
            self.touch_write(self.coords_TA["pos_x"], data_view_x)
            self.touch_write(self.coords_TA["pos_y"], data_view_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Menu Touch Error")
            
    def btn_popup_touch(self, btn_popup_key):
        if self.client_check:
            btn_x, btn_y = self.coords_touch[btn_popup_key]
            self.touch_write(self.coords_TA["pos_x"], btn_x)
            self.touch_write(self.coords_TA["pos_y"], btn_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Button Popup Touch Error")
            
    def number_1_touch(self, number_key):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key]
            self.touch_write(self.coords_TA["pos_x"], number_x)
            self.touch_write(self.coords_TA["pos_y"], number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")
            
    def number_2_touch(self, number_key1, number_key2):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(self.coords_TA["pos_x"], number_x)
            self.touch_write(self.coords_TA["pos_y"], number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(self.coords_TA["pos_x"], number_a)
            self.touch_write(self.coords_TA["pos_y"], number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")
            
    def number_3_touch(self, number_key1, number_key2, number_key3):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(self.coords_TA["pos_x"], number_x)
            self.touch_write(self.coords_TA["pos_y"], number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(self.coords_TA["pos_x"], number_a)
            self.touch_write(self.coords_TA["pos_y"], number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_c, number_d = self.coords_touch[number_key3]
            self.touch_write(self.coords_TA["pos_x"], number_c)
            self.touch_write(self.coords_TA["pos_y"], number_d)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")
            
    def btn_apply_touch(self):
        if self.client_check:
            self.touch_write(self.coords_TA["pos_x"], self.coords_touch["btn_apply"][0])
            self.touch_write(self.coords_TA["pos_y"], self.coords_touch["btn_apply"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Button Apply Touch Error")
        
    
class OCRImageManager:
    
    rois = config_data.roi_params()
    
    def __init__(self):
        self.use_gpu = torch.cuda.is_available()
    
    
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
    
    def color_detection(self, image, x, y, w, h, R, G, B):
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            selected_area = image_rgb[y:y+h, x:x+w]
            average_color = np.mean(selected_area, axis=(0, 1))
            target_color = np.array([R, G, B])
            color_difference = np.linalg.norm(average_color - target_color)
            return color_difference
    
    def image_cut_custom(self, image, roi_keys):
        image = cv2.imread(image)
        resized_image = cv2.resize(image, None, None, 3, 3, cv2.INTER_CUBIC)
        blurred_image = cv2.GaussianBlur(resized_image, (0, 0), 3)
        sharpened_image = cv2.addWeighted(resized_image, 1.5, blurred_image, -0.5, 0)
        reader = easyocr.Reader(['en'], gpu=self.use_gpu)

        # 각 ROI에 대해 OCR 처리 및 결과 수집
        ocr_results = {}
        for roi_key in roi_keys:
            if roi_key in self.rois:
                x, y, w, h = self.rois[roi_key]
                roi_image = sharpened_image[y:y+h, x:x+w]
                # cv2.imshow('Image with Size Info', roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                text_results = reader.readtext(roi_image, paragraph=False)  # 해당 ROI에 대해 OCR 수행
                # 추출된 텍스트 합치기
                # extracted_texts = ' '.join([text[1] for text in text_results])
                
                # 추출된 텍스트 합치기 and 대체
                extracted_texts = ' '.join([text[1].replace(':', '.') for text in text_results])
                ocr_results[roi_key] = extracted_texts

        # OCR 결과 출력
        for roi_key, text in ocr_results.items():
            print(f'ROI {roi_key}: {text}')

        ocr_results_list = [text for text in ocr_results.values() if text]
        # print(f"OCR Results: {ocr_results_list}")
        return ocr_results_list 

class ModbusLabels:
    
    mobus_manager = ModbusManager()
    setup_client = mobus_manager.setup_client
    meter_m_vol_mappings_value, meter_m_vol_mappings_uint16, meter_m_vol_mappings_uint32 = config_data.meter_m_vol_mapping()
    meter_m_cur_mappings_value, meter_m_cur_mappings_uint16, meter_m_cur_mappings_uint32 = config_data.meter_m_cur_mapping()
    
    def read_all_modbus_values(self):
        self.read_results = {}
        for address, info in self.meter_m_vol_mappings_value.items():
            result = self.read_modbus_value(address, self.meter_m_vol_mappings_value)
            ### self.results를 self.read_results로 바꿀껀데 검증 필요함
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_vol_mappings_uint16.items():
            result = self.read_uint16(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_vol_mappings_uint32.items():
            result = self.read_uint32(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_value.items():
            result = self.read_modbus_value(address, self.meter_m_cur_mappings_value)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_uint16.items():
            result = self.read_uint16(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_uint32.items():
            result = self.read_uint32(address)
            self.read_results[info["description"]] = result
        return self.read_results

    def read_modbus_value(self, address, mapping):
        response = self.setup_client.read_holding_registers(address, count=1)
        if response.isError():
            print("Error reading VALUE", address)
            return None
        else:
            value = response.registers[0]
            return mapping[address]["values"].get(value, "Unknown Value")
        
    def read_uint16(self, address):
        response = self.setup_client.read_holding_registers(address, count=1)
        if response.isError():
            print("Error reading UINT16", address)
            return None
        else:
            value = response.registers[0]
            return value
        
    def read_uint32(self, address):
        response = self.setup_client.read_holding_registers(address, count=2)
        if response.isError():
            print("Error reading UINT32", address)
            return None
        else:
            high_register = response.registers[0]
            low_register = response.registers[1]
            value = (low_register << 16) + high_register 
            return value
        
    def check_for_changes(self, initial_values):
        if self.read_results:
            current_values = self.read_results
            changes = {}
            for description, current_value in current_values.items():
                initial_value = initial_values.get(description)
                if initial_value != current_value:
                    changes[description] = (initial_value, current_value)
            return changes
        else:
            print("read_results is empty")

    def display_changes(self, initial_values):
        changes = self.check_for_changes(initial_values)
        change_count = len(changes)
        if changes:
            print("Changes detected:")
            for description, (initial, current) in changes.items():
                print(f"Address {description}: Initial Value = {initial}, Current Value = {current}")
        else:
            print("No changes detected.")
        return change_count
        
class Evaluation:

    label_voltage, label_current, label_demand, label_power, label_dip, label_swell, label_pqcurve, label_Ethernet, label_RS485, label_Advanced = config_data.match_labels()

    def evaluation_ocr(self, ocr_results_1, right_list):

            ocr_right_1 = right_list

            right_list_1 = [text.strip() for text in ocr_right_1]
            ocr_list_1 = [result.strip() for result in ocr_results_1]
            
            leave_ocr_all = [result for result in ocr_list_1 if result not in right_list_1]
            leave_right_all = [text for text in right_list_1 if text not in ocr_list_1]
            
            ocr_error = leave_ocr_all
            right_error = leave_right_all

            
            # OCR 결과와 매칭되지 않아 남은 단어
            print(f"OCR 결과와 매칭되지 않는 단어들: {ocr_error}")
            print(f"\n정답 중 OCR 결과와 매칭되지 않는 단어들: {right_error}")
            
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

