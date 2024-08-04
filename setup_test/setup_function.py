from os import error
from re import template
import threading
import time
import numpy as np
import cv2
from datetime import datetime
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import torch
import os
import pandas as pd
from paddleocr import PaddleOCR

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

    def btn_front_setup(self):
        if self.client_check:
            self.touch_write(self.coords_TA["setup_button"], 1)
            self.touch_write(self.coords_TA["setup_button_bit"], 2)
        else:
            print("Button Apply Touch Error")
    
    def btn_front_meter(self):
        if self.client_check:
            self.touch_write(self.coords_TA["setup_button"], 1)
            self.touch_write(self.coords_TA["setup_button_bit"], 64)
        else:
            print("Button Apply Touch Error")

    def btn_front_home(self):
        if self.client_check:
            self.touch_write(self.coords_TA["setup_button"], 1)
            self.touch_write(self.coords_TA["setup_button_bit"], 1)
        else:
            print("Button Apply Touch Error")
   
class OCRManager:
    
    rois = config_data.roi_params()
    
    def __init__(self):
        self.use_gpu = torch.cuda.is_available()
    
    
    ########################## 이미지 커팅 기본 method ##########################
    def image_cut(self, image, height_ratio_start, height_ratio_end, width_ratio_start, width_ratio_end):
        height, width = image.shape[:2]
        cropped_image = image[int(height*height_ratio_start):int(height*height_ratio_end),
                            int(width*width_ratio_start):int(width*width_ratio_end)]
        resized_image = cv2.resize(cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        ### 이미지 필터 ###
        # gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        # _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        # alpha = 10.0 # Contrast control
        # beta = -100 # Brightness control
        # adjusted_image = cv2.convertScaleAbs(binary_image, alpha=alpha, beta=beta)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        # morph_image = cv2.morphologyEx(adjusted_image, cv2.MORPH_CLOSE, kernel)
        # denoised_image = cv2.fastNlMeansDenoising(morph_image, None, 30, 7, 21)
        
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
    
    def ocr_basic(self, image, roi_keys):
        image = cv2.imread(image)
        resized_image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        denoised_image = cv2.fastNlMeansDenoising(resized_image, None, 30, 7, 21)

        ocr = PaddleOCR(use_angle_cls=False, lang='en', use_space_char=True, show_log=False,)  

        ocr_results = {}
        for roi_key in roi_keys:
            if roi_key in self.rois:
                x, y, w, h = self.rois[roi_key]
                roi_image = denoised_image[y:y+h, x:x+w]
                # cv2.imshow('Image with Size Info', roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                text_results = ocr.ocr(roi_image, cls=False)
                extracted_texts = ' '.join([text[1][0] for line in text_results for text in line])
                ocr_results[roi_key] = extracted_texts

        # OCR 결과 출력
        for roi_key, text in ocr_results.items():
            print(f'ROI {roi_key}: {text}')

        ocr_results_list = [text for text in ocr_results.values() if text]
        return ocr_results_list

class ModbusLabels:
    
    modbus_manager = ModbusManager()
    touch_manager = TouchManager()
    setup_client = modbus_manager.setup_client
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
    
    def demo_test_setting(self):
        self.touch_manager.uitest_mode_start()
        addr_setup_lock = 2900
        addr_control_lock = 2901
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value in values:
                self.response = self.modbus_manager.setup_client.write_register(addr_setup_lock, value)
                time.sleep(0.6)
            value_32bit = 1900
            high_word = (value_32bit >> 16) & 0xFFFF  # 상위 16비트
            low_word = value_32bit & 0xFFFF  
            self.response = self.modbus_manager.setup_client.write_register(6001, 0)
            self.response = self.modbus_manager.setup_client.write_registers(6003, [high_word, low_word])
            self.response = self.modbus_manager.setup_client.write_registers(6005, [high_word, low_word])
            self.response = self.modbus_manager.setup_client.write_registers(6007, 1900)
            self.response = self.modbus_manager.setup_client.write_register(6009, 0)
            self.response = self.modbus_manager.setup_client.write_register(6000, 1)
            time.sleep(0.6)
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(4002, 0)
            self.response = self.modbus_manager.setup_client.write_register(4000, 1)
            self.response = self.modbus_manager.setup_client.write_register(4001, 1)
            print("Done")
        else:
            print(self.response.isError())
        
class Evaluation:
    
    MM_clear_time = None

    def __init__(self):
        self.labels = config_data.match_m_setup_labels()
        self.pop_params = config_data.match_pop_labels()
        self.m_home, self.m_setup = config_data.match_m_setup_labels()

        pass

    
    def eval_static_text(self, ocr_results_1, right_key):
        
        right_list = self.pop_params[right_key]
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
    
    def eval_variable_text(self, ocr_results_1, right_list):
    
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
    
    def eval_demo_test(self, ocr_res, right_key, ocr_res_meas):
        
        meas_error = False

        ocr_right = self.m_home[right_key]

        right_list = [text.strip() for text in ocr_right]
        ocr_rt_list = [result.strip() for result in ocr_res]
        
        self.ocr_error = [result for result in ocr_rt_list if result not in right_list]
        right_error = [text for text in right_list if text not in ocr_rt_list]

        if self.ocr_error and "RMS" in self.ocr_error[0]:
            values = ['A', 'B', 'C', 'Aver']
            results = {name: float(value) for name, value in zip(values, ocr_res_meas)}
            for name, value in results.items():
                if 189.62 < value < 190.38:
                    print(f"{name} = PASS")
                else:
                    print(f"{name} = {value}")
                    meas_error = True
        
        if self.ocr_error and "Total" in self.ocr_error[0]:
            values = ['A', 'B', 'C']
            results = {name: float(value) for name, value in zip(values, ocr_res_meas)}
            for name, value in results.items():
                if -1.0 < value < 1.0:
                    print(f"{name} = PASS")
                else:
                    print(f"{name} = {value}")
                    meas_error = True

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")
        
        return self.ocr_error, right_error, meas_error
    
    def check_time_diff(self, time_images):
        if not self.MM_clear_time:
            self.MM_clear_time = datetime.now()

        time_format = "%Y-%m-%d %H:%M:%S"
        failed_times = []
        for time_str in time_images:
            try:
                image_time = datetime.strptime(time_str, time_format)
                time_diff = abs((image_time - self.MM_clear_time).total_seconds())
                if time_diff <= 5 * 60:
                    print(f"{time_str} = PASS")
                else:
                    print(f"{time_str} = {time_diff} seconds = FAIL")
                    failed_times.append(time_str)
            except ValueError as e:
                print(f"Time format error for {time_str}: {e}")
        if failed_times:
            return failed_times
        return None
    
    def img_match(self, image, roi_key):
        if self.ocr_error and "Phasor" in self.ocr_error[0]:
            template_image_path= r"C:\Users\Jin\Desktop\Company\Rootech\PNT\AutoProgram\image_test\A3700N_phaser_demo_1.png"
        elif self.ocr_error and "Harmonics" in self.ocr_error[0]:
            template_image_path= r"C:"
        elif self.ocr_error and "Waveform" in self.ocr_error[0]:
            template_image_path= r"C:"
        image = cv2.imread(image)
        template_image = cv2.imread(template_image_path)
        x, y, w, h = roi_key
        cut_img = image[y:y+h, x:x+w]
        resized_cut_img = cv2.resize(cut_img, (template_image.shape[1], template_image.shape[0]))
        res = cv2.matchTemplate(resized_cut_img, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        print(max_val)
    
    def save_csv(self, ocr_img, ocr_error, right_error, meas_error=False, ocr_img_meas=None, ocr_img_time=None, time_error=None):
        ocr_img_meas = ocr_img_meas if ocr_img_meas is not None else []
        ocr_img_time = ocr_img_time if ocr_img_time is not None else []
        time_error = time_error if time_error is not None else []
        
        num_entries = max(len(ocr_img), len(ocr_img_meas), len(ocr_img_time))
    
        csv_results = {
            "Main View": ocr_img + [None] * (num_entries - len(ocr_img)),
            "Measurement Accuracy": ocr_img_meas + [None] * (num_entries - len(ocr_img_meas)),
            "OCR-Right": [ocr_error] * num_entries,
            "Right-OCR": [right_error] * num_entries,
            "Time Stemp Error": time_error + [None] * (num_entries - len(time_error)),
        }
        
        df = pd.DataFrame(csv_results)
        if not ocr_error and not right_error and not time_error and not meas_error:
            save_path = os.path.expanduser(f"./csvtest/PASS_ocr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        else:
            save_path = os.path.expanduser(f"./csvtest/FAIL_ocr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        df.to_csv(save_path, index=False)
