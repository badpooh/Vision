from os import error
import re
import threading
import time
import numpy as np
import cv2
from datetime import datetime
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import shutil
# import torch
import os
import pandas as pd
from paddleocr import PaddleOCR

from demo_test.demo_config import ConfigSetup
from demo_test.demo_config import ConfigTextRef as ec
from demo_test.demo_config import ConfigROI as ecr
from demo_test.demo_config import ConfigImgRef as ecir
from demo_test.demo_config import ConfigModbusMap as ecm
from demo_test.demo_config import ConfigTouch as ect

config_data = ConfigSetup()


class ModbusManager:

    SERVER_IP = '10.10.26.159'  # 장치 IP 주소
    TOUCH_PORT = 5100  # 내부터치
    SETUP_PORT = 502  # 설정

    def __init__(self):
        self.is_connected = False
        self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
        self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)

    def tcp_connect(self):
        if self.touch_client.connect() and self.setup_client.connect():
            self.is_connected = True
            print("is connected")
        else:
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
        print(f"Failed to write value {value} to address {
              address}. Read back {read_value} instead.")

    def uitest_mode_start(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_ui_test_mode.value, 1)
        else:
            print("client Error")

    def screenshot(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_screen_capture.value, self.hex_value)
        else:
            print("client Error")

    def menu_touch(self, menu_key):
        if self.client_check:
            data_view_x, data_view_y = menu_key
            self.touch_write(ect.touch_addr_pos_x.value, data_view_x)
            self.touch_write(ect.touch_addr_pos_y.value, data_view_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Menu Touch Error")

    def btn_popup_touch(self, btn_popup_key):
        if self.client_check:
            btn_x, btn_y = self.coords_touch[btn_popup_key]
            self.touch_write(ect.touch_addr_pos_x.value, btn_x)
            self.touch_write(ect.touch_addr_pos_y.value, btn_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Popup Touch Error")

    def number_1_touch(self, number_key):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(
                ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_2_touch(self, number_key1, number_key2):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_3_touch(self, number_key1, number_key2, number_key3):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_c, number_d = self.coords_touch[number_key3]
            self.touch_write(ect.touch_addr_pos_x.value, number_c)
            self.touch_write(ect.touch_addr_pos_y.value, number_d)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def btn_apply_touch(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_apply"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_apply"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Apply Touch Error")

    def btn_front_setup(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 2)
        else:
            print("Button Apply Touch Error")

    def btn_front_meter(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 64)
        else:
            print("Button Apply Touch Error")

    def btn_front_home(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 1)
        else:
            print("Button Apply Touch Error")

class OCRManager:

    rois = config_data.roi_params()

    def __init__(self):
        pass

    def color_detection(self, image, color_data):
        x, y, w, h, R, G, B = color_data
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        selected_area = image_rgb[y:y+h, x:x+w]
        average_color = np.mean(selected_area, axis=(0, 1))
        target_color = np.array([R, G, B])
        color_difference = np.linalg.norm(average_color - target_color)
        return color_difference

    def ocr_basic(self, image, roi_keys):
        image = cv2.imread(image)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {image}")
            return []
        
        resized_image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 30, 30, 7, 21)
        
        ocr = PaddleOCR(use_angle_cls=False, lang='en', use_space_char=True, show_log=False)  
        
        ocr_results = {}
        for roi_key in roi_keys:
            if roi_key in self.rois:
                x, y, w, h = self.rois[roi_key]
                roi_image = resized_image[y:y+h, x:x+w]
                
                # ROI 이미지 표시 (디버깅용)
                # cv2.imshow('ROI Image', roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

                text_results = ocr.ocr(roi_image, cls=False)
                
                if text_results:
                    extracted_texts = ' '.join(
                        ['empty' if line is None else ' '.join([text[1][0] if text is not None else 'empty' for text in line])
                        for line in text_results])
                else:
                    extracted_texts = "empty"
                ocr_results[roi_key] = extracted_texts
   
        for roi_key, text in ocr_results.items():
            print(f'{roi_key}: {text}')
        
        # 유효한 텍스트만 리스트로 반환
        ocr_results_list = [text for text in ocr_results.values() if text]
        return ocr_results_list

class ModbusLabels:

    touch_manager = TouchManager()
    modbus_manager = ModbusManager()

    def __init__(self):
        pass

    def demo_test_setting(self):
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value in values:
                self.response = self.modbus_manager.setup_client.write_register(ecm.addr_setup_lock.value, value)
                time.sleep(0.6)
            vol_value_32bit = 1900
            high_word = (vol_value_32bit >> 16) & 0xFFFF  # 상위 16비트
            low_word = vol_value_32bit & 0xFFFF
            self.response = self.modbus_manager.setup_client.read_holding_registers(6000, 100)
            self.response = self.modbus_manager.setup_client.read_holding_registers(6100, 100)
            self.response = self.modbus_manager.setup_client.read_holding_registers(6200, 3)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.modbus_manager.setup_client.write_register(6001, 0)
            self.response = self.modbus_manager.setup_client.write_registers(6003, [high_word, low_word])
            self.response = self.modbus_manager.setup_client.write_registers(6005, [high_word, low_word])
            self.response = self.modbus_manager.setup_client.write_registers(6007, 1900)
            self.response = self.modbus_manager.setup_client.write_register(6009, 0)
            self.response = self.modbus_manager.setup_client.write_register(6000, 1)
            time.sleep(0.6)
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(4002, 0)
            self.response = self.modbus_manager.setup_client.write_register(4000, 1)
            self.response = self.modbus_manager.setup_client.write_register(4001, 1)
            print("Done")
        else:
            print(self.response.isError())
    
    def reset_max_min(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_reset_max_min.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
        self.reset_time = datetime.now()
        return self.reset_time
    
    def reset_demand(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_reset_demand.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
    
    def reset_demand_peak(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(ecm.addr_control_lock.value, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_reset_demand_peak.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
        self.reset_time = datetime.now()
        return self.reset_time
    
    def demo_test_demand(self):
        self.touch_manager.uitest_mode_start()
        addr_control_lock = 2901
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.modbus_manager.setup_client.read_holding_registers(6000, 1)
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_demand_sync_mode.value, 1)
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_demand_sub_interval_time.value, 2)
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_demand_num_of_sub_interval.value, 3)
            demand_reset_time = self.reset_demand_peak()
            self.reset_demand()
            self.response = self.modbus_manager.setup_client.write_register(ecm.addr_demand_sync.value, 1)
        else:
            print(self.response.isError())
            
        return demand_reset_time
        

class Evaluation:

    reset_time = None
    ocr_manager = OCRManager()
    rois = config_data.roi_params()

    def __init__(self):
        self.m_home, self.m_setup = config_data.match_m_setup_labels()

    def eval_demo_test(self, ocr_res, right_key, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        color_data = config_data.color_detection_data()
        
        image = cv2.imread(image_path)

        ocr_right = right_key

        right_list = ' '.join(text.strip() for text in ocr_right).split()
        ocr_rt_list = ' '.join(result.strip() for result in ocr_res).split()

        right_set = set(right_list)
        ocr_rt_set = set(ocr_rt_list)

        self.ocr_error = list(ocr_rt_set - right_set)
        right_error = list(right_set - ocr_rt_set)

        def check_results(values, limits, ocr_meas_subset):
            self.condition_met = True
            meas_results = []

            if isinstance(ocr_meas_subset, (float, int)):
                results = {values[0]: str(ocr_meas_subset)}
            elif isinstance(ocr_meas_subset, list):
                results = {name: str(value) for name, value in zip(values, ocr_meas_subset)}
            else:
                print("Unexpected ocr_meas_subset type.")
                return

            for name, value in results.items():
                match = re.match(r"([-+]?\d+\.?\d*)\s*(\D*)", value)
                if match:
                    numeric_value = float(match.group(1))  # 숫자 부분
                    unit = match.group(2)  # 단위 부분 (예: V)
                else:
                    numeric_value = None
                    unit = value.strip()

                    # 텍스트 정답을 처리하는 로직 추가
                text_matches = [lim for lim in limits if isinstance(lim, str)]
                if any(text_match == value for text_match in text_matches):
                    print(f"{name or 'empty'} = {value} (PASS by text match)")
                    meas_results.append(f"{name or 'empty'} = {value} (PASS by text)")
                    
                elif numeric_value is not None and len(limits) >= 3 and isinstance(limits[0], (int, float)):
                    if limits[0] <= numeric_value <= limits[1] and limits[2] == unit:
                        print(f"{name} = {numeric_value}{unit} (PASS)")
                        meas_results.append(f"{numeric_value}{unit} (PASS)")
                    else:
                        print(f"{name} = {value} (FAIL)")
                        meas_results.append(f"{value} (FAIL)")
                        self.meas_error = True
                else:
                    print(f"{name} = {value} (FAIL)")
                    meas_results.append(f"{value} (FAIL)")
                    self.meas_error = True
            return meas_results
        
        all_meas_results = []

        if "RMS Voltage" in ''.join(ocr_res[0]) or "Fund. Volt." in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (180, 200, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, ecr.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (100, 120, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, ecr.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (2.0, 4.0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, ecr.color_vol_thd_ln.value) <= 10:
                    all_meas_results.extend(check_results(["A", "B", "C"], (3.0, 4.0, "%"), ocr_res_meas[:4]))
                else:
                    print("Total Harmonic missed")

        elif "Frequency" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["Freq"], (59, 61, "Hz"), ocr_res_meas[:1]))

        elif "Residual Voltage" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS", "Fund."], (0, 10, "V"), ocr_res_meas[:2]))

        elif "RMS Current" in ''.join(ocr_res[0]) or "Fundamental Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Aver %"], (45, 55, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (2, 3, "A"), ocr_res_meas[4:]))

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_main_menu_curr.value) <= 10: 
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 3.0, "%"), ocr_res_meas[:3]))

        elif "Total Demand" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (1, 2.5, "%"), ocr_res_meas[:3]))

        elif "Crest Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (1.3, 1.6, ""), ocr_res_meas[:3]))

        elif "K-Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (1.2, 1.5, ""), ocr_res_meas[:3]))

        elif "Residual Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS"], (70, 100, "mA"), ocr_res_meas[:1]))
            all_meas_results.extend(check_results(["RMS"], (20, 40, "mA"), ocr_res_meas[1:2]))
            
        elif "Active Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Total %"], (40, 50, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (230, 240, "W"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (705, 715, "W"), ocr_res_meas[7:8]))
            
        elif "Reactive Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(20, 30, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (130, 145, "VAR"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (400, 420, "VAR"), ocr_res_meas[7:8]))
            
        elif "Apparent Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A', 'B', 'C', 'Total'],(45, 55, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (270, 280, "VA"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (810, 830, "VA"), ocr_res_meas[7:8]))
            
        elif "Power Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(45, 55, "Lag"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Total"], (0.860, 0.870, ""), ocr_res_meas[4:8]))
            
        elif "Phasor" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (180, 195, "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (25, 35, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (-95, -85, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (145, 155, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([ecir.img_ref_phasor_all_vll.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, ecr.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (100, 120, "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (-0.2, 5, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (-125, -115, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (115, 125, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([ecir.img_ref_phasor_all_vln.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_harmonics_vol.value) <= 10:
                if img_result == 1 or img_result == 0:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (1, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.95, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    all_meas_results.extend("PASS?")
                else:
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (3.0, 4.0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
            else:
                if img_result == 1 or img_result == 0:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (1, 1, ""), img_result))  
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.95, 1, ""), img_result))
                else:
                    all_meas_results.extend(check_results(["CURR_A_THD", "CURR_B_THD", "CURR_C_THD"], (1.5, 2.5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["CURR_A_Fund", "CURR_B_Fund", "CURR_C_Fund"], (2, 3, "A"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.98, 1, ""), img_result))
                    
        elif "Waveform" in ''.join(ocr_res[0]):
            if 0 < img_result < 1:
                all_meas_results.extend(check_results(["waveform_image"], (0.945, 1, ""), img_result))
            else:
                all_meas_results.extend(check_results(["waveform_img_detect"], (1, 1, ""), img_result))
                
        elif "Volt. Symm. Component" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (180, 200, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (180, 200, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (180, 200, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 1, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, ecr.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (180, 200, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (180, 200, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V0'], (180, 200, "V0"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V1'], (100, 110, "V" or "v"), ocr_res_meas[3:4]))
                all_meas_results.extend(check_results(['V2'], (0, 2, "V" or "v"), ocr_res_meas[4:5]))
                all_meas_results.extend(check_results(['V0'], (0, 1, "V" or "v"), ocr_res_meas[5:6]))
                
        elif "Voltage Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["NEMA LL"], (0, 1, "LL"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["NEMA LN"], (0, 1, "LN"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U2"], (0, 1, "U2"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["U0"], (0, 1, "U0"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["NEMA LL", "NEMA LN", "U2", "U0"], (0, 1, "%"), ocr_res_meas[4:8]))
            
        elif "Curr. Symm. Component" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["I1"], (0, 1, "l1"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["I2"], (0, 1, "l2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["I0"], (0, 1, "l0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["I1"], (2, 3, "A"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["I2"], (0, 0.1, "A"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["I0"], (0, 0.1, "A"), ocr_res_meas[5:6]))
            
        elif "Current Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results([""], (0, 1, "empty"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["U2"], (0, 1, "U2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U0"], (0, 1, "U0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results([""], (0, 1, "%"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["U2"], (0, 1, "%"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["U0"], (0, 0.5, "%"), ocr_res_meas[5:6]))
        
        elif not self.condition_met:
            print("Nothing matching word")

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")

        return self.ocr_error, right_error, self.meas_error, ocr_res, all_meas_results,
    
    def check_text(self, ocr_results):
        results = []
        
        for value in ocr_results:
            if value.replace('.', '', 1).isdigit():
                result = f"{value} (PASS)"
            else:
                result = f"{value} (FAIL)"
            
            # 결과 리스트에 추가
            results.append(result)
        
        # 결과를 하나의 문자열로 합치기
        final_result = ", ".join(results)
        print(final_result)
        
        return final_result
    
    def img_match(self, image, roi_key, tpl_img_path):
            template_image_path = tpl_img_path
            image = cv2.imread(image)
            template_image = cv2.imread(template_image_path)
            x, y, w, h = self.rois[roi_key]
            # print(f"ROI coordinates: x={x}, y={y}, w={w}, h={h}")
            # print(f"Original image size: {image.shape}")
            # print(f"Template image size: {template_image.shape}")
            cut_img = image[y:y+h, x:x+w]
            cut_template = template_image[y:y+h, x:x+w]

            resized_cut_img = cv2.resize(
                cut_img, (cut_template.shape[1], cut_template.shape[0]))
            res = cv2.matchTemplate(
                resized_cut_img, cut_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            print(max_val)
            
            return max_val
    
    def img_detection(self, image_path, color_data, tolerance):
        image = cv2.imread(image_path)
        x, y, w, h, R, G, B = color_data
        cut_img = image[y:y+h, x:x+w]

        # cv2.imshow('Image', cut_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        target_color = np.array([B, G, R])
        diff = np.abs(cut_img - target_color)
        match = np.all(diff <= tolerance, axis=2)

        if np.array_equal(target_color, np.array([0, 0, 0])):
            target_color = "Vol_A(X)"
        elif np.array_equal(target_color, np.array([37, 29, 255])):  # BGR 순서로 비교
            target_color = "Vol_B(X)"
        elif np.array_equal(target_color, np.array([255, 0, 0])):
            target_color = "Vol_C(X)"
        elif np.array_equal(target_color, np.array([153, 153, 153])):
            target_color = "Curr_A(X)"
        elif np.array_equal(target_color, np.array([245, 180, 255])):  # BGR 순서로 비교
            target_color = "Curr_B(X)"
        elif np.array_equal(target_color, np.array([255, 175, 54])):  # BGR 순서로 비교
            target_color = "Curr_C(X)"

        if np.any(match):
            print(f"{target_color} (FAIL)")
            result = 0
        else:
            print(f"{target_color} (PASS)")
            result = 1
        return result

    def check_time_diff(self, time_images, reset_time):
        self.reset_time = reset_time
        if not self.reset_time:
            self.reset_time = datetime.now()

        time_format = "%Y-%m-%d %H:%M:%S"
        results = []
        for time_str in time_images:
            try:
                image_time = datetime.strptime(time_str, time_format)
                time_diff = abs(
                    (image_time - self.reset_time).total_seconds())
                if time_diff <= 5 * 60:
                    print(f"{time_str} (PASS)")
                    results.append(f"{time_str} (PASS)")
                else:
                    print(f"{time_str} / {time_diff} seconds (FAIL)")
                    results.append(f"{time_str} / {time_diff} seconds (FAIL)")      
            except ValueError as e:
                print(f"Time format error for {time_str}: {e}")
                results.append(f"Time format error for {time_str}: {e}")
        return results

    def save_csv(self, ocr_img, ocr_error, right_error, meas_error=False, ocr_img_meas=None, ocr_img_time=None, time_results=None, img_path=None, img_result=None, base_save_path=None, all_meas_results=None, invalid_elements=None):
        ocr_img_meas = ocr_img_meas if ocr_img_meas is not None else []
        ocr_img_time = ocr_img_time if ocr_img_time is not None else []
        time_results = time_results if time_results is not None else []
        img_result = [img_result]

        if invalid_elements is None:
            invalid_elements = []

        if ocr_img_meas == bool:
            ocr_img_meas = []
            num_entries = max(len(ocr_img), len(ocr_img_meas)+1, len(ocr_img_time)+1, len(img_result)+1)
        else:
            num_entries = max(len(ocr_img), len(ocr_img_meas)+1, len(ocr_img_time)+1, len(img_result)+1)

        overall_result = "PASS"
        if ocr_error or right_error or meas_error:
            overall_result = "FAIL"
        if any("FAIL" in result for result in time_results):
            overall_result = "FAIL"
        
        if all_meas_results is not None:
            measurement_results = [f"{meas}" for meas in all_meas_results]
            if len(measurement_results) < num_entries:
                measurement_results = [None] + measurement_results + [None] * (num_entries - len(measurement_results) - 1)
            
            csv_results = {
            "Main View": ocr_img + [None] * (num_entries - len(ocr_img)),
            "Measurement": measurement_results,
            "OCR-Right": [None] + [f"{ocr_error} ({'FAIL' if ocr_error else 'PASS'})"] + [""]* (num_entries-2),
            "Right-OCR": [None] + [f"{right_error} ({'FAIL' if right_error else 'PASS'})"] + [""]* (num_entries-2),
            f"Time Stemp ({self.reset_time})": [None] + time_results + [None] * (num_entries - len(time_results)-1),
            "Img Match": [None] + img_result + [None] * (num_entries-len(img_result)-1),
            "H.Text": [None] + invalid_elements + [None] * (num_entries-len(img_result)-1),
            }
        
        else:
            csv_results = {
            "Main View": ocr_img + [None] * (num_entries - len(ocr_img)),
            "OCR-Right": [None] + [f"{ocr_error} ({'FAIL' if ocr_error else 'PASS'})"] + [""]* (num_entries-2),
            "Right-OCR": [None] + [f"{right_error} ({'FAIL' if right_error else 'PASS'})"] + [""]* (num_entries-2),
            f"Time Stemp ({self.reset_time})": [None] + time_results + [None] * (num_entries - len(time_results)-1),
            "Img Match": [None] + img_result + [None] * (num_entries-len(img_result)-1),
            "H.Text": [None] + invalid_elements + [None] * (num_entries-len(img_result)-1),
            }
        
        
        # Ensure all columns have the same length
        for key in csv_results:
            csv_results[key] = csv_results[key][:num_entries]
            if len(csv_results[key]) < num_entries:
                csv_results[key].extend([None] * (num_entries - len(csv_results[key])))

        df = pd.DataFrame(csv_results)

        # Saving the CSV
        file_name_with_extension = os.path.basename(img_path)
        ip_to_remove = "10.10.26.159_"
        if file_name_with_extension.startswith(ip_to_remove):
            file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
        else:
            file_name_without_ip = file_name_with_extension

        image_file_name = os.path.splitext(file_name_without_ip)[0]
        
        save_path = os.path.join(base_save_path, f"{overall_result}_ocr_{image_file_name}.csv")

        df.to_csv(save_path, index=False)
        dest_image_path = os.path.join(base_save_path, file_name_without_ip)
        shutil.copy(img_path, dest_image_path)

    def count_csv_and_failures(self, folder_path):
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        total_csv_files = len(csv_files)

        fail_count = sum(1 for f in csv_files if 'FAIL' in f)

        return total_csv_files, fail_count
    
    def validate_ocr(self, ocr_img):     
        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        def process_text(text):
            elements = text.split()
            numbers = []
            invalid_elements = []

            for elem in elements:
                if is_float(elem):
                    numbers.append(float(elem))
                else:
                    invalid_elements.append(elem)
            return numbers, invalid_elements

        for result in ocr_img:
            numbers, invalid_elements = process_text(result)
            
            if invalid_elements:
                print(f"FAIL: {invalid_elements}")
            else:
                print("PASS")
            
            print(f"추출된 숫자: {numbers}")
        return invalid_elements
