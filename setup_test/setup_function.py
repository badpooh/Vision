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

from setup_test.setup_config import ConfigSetup
from setup_test.setup_config import EnumConfig as ec

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
        print(f"Failed to write value {value} to address {
              address}. Read back {read_value} instead.")

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
            self.touch_write(
                self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
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
            self.touch_write(
                self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
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
            self.touch_write(
                self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
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
            self.touch_write(
                self.coords_TA["pos_x"], self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                self.coords_TA["pos_y"], self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def btn_apply_touch(self):
        if self.client_check:
            self.touch_write(
                self.coords_TA["pos_x"], self.coords_touch["btn_apply"][0])
            self.touch_write(
                self.coords_TA["pos_y"], self.coords_touch["btn_apply"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Button Apply Touch Error")

    def btn_front_setup(self):
        if self.client_check:
            self.touch_write(self.coords_TA["setup_button"], 0)
            self.touch_write(self.coords_TA["setup_button_bit"], 2)
        else:
            print("Button Apply Touch Error")

    def btn_front_meter(self):
        if self.client_check:
            self.touch_write(self.coords_TA["setup_button"], 0)
            self.touch_write(self.coords_TA["setup_button_bit"], 64)
        else:
            print("Button Apply Touch Error")

    def btn_front_home(self):
        if self.client_check:
            self.touch_write(self.coords_TA["setup_button"], 0)
            self.touch_write(self.coords_TA["setup_button_bit"], 1)
        else:
            print("Button Apply Touch Error")


class OCRManager:

    rois = config_data.roi_params()

    def __init__(self):
        pass
        # self.use_gpu = torch.cuda.is_available()

    ########################## 이미지 커팅 기본 method ##########################

    def image_cut(self, image, height_ratio_start, height_ratio_end, width_ratio_start, width_ratio_end):
        height, width = image.shape[:2]
        cropped_image = image[int(height*height_ratio_start):int(height*height_ratio_end),
                              int(width*width_ratio_start):int(width*width_ratio_end)]
        resized_image = cv2.resize(
            cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

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
        sharpened_image = cv2.addWeighted(
            resized_image, 1.5, blurred_image, -0.5, 0)
        return sharpened_image
    ####################################################

    def color_detection(self, image, color_data):
        x, y, w, h, R, G, B = color_data
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        selected_area = image_rgb[y:y+h, x:x+w]
        average_color = np.mean(selected_area, axis=(0, 1))
        target_color = np.array([R, G, B])
        color_difference = np.linalg.norm(average_color - target_color)
        return color_difference

    def ocr_basic(self, image, roi_keys):
        # 이미지 읽기 및 전처리
        image = cv2.imread(image)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {image}")
            return []
        
        resized_image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 30, 30, 7, 21)
        
        # OCR 객체 초기화
        ocr = PaddleOCR(use_angle_cls=False, lang='en', use_space_char=True, show_log=False)  
        
        ocr_results = {}
        for roi_key in roi_keys:
            if roi_key in self.rois:
                x, y, w, h = self.rois[roi_key]
                roi_image = gray_image[y:y+h, x:x+w]
                
                # ROI 이미지 표시 (디버깅용)
                # cv2.imshow('ROI Image', roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                # OCR 수행
                text_results = ocr.ocr(roi_image, cls=False)
                
                if text_results:
                    extracted_texts = ' '.join(
                        ['empty' if line is None else ' '.join([text[1][0] if text is not None else 'empty' for text in line])
                        for line in text_results])
                else:
                    extracted_texts = "empty"
                ocr_results[roi_key] = extracted_texts
   
        for roi_key, text in ocr_results.items():
            print(f'ROI {roi_key}: {text}')
        
        # 유효한 텍스트만 리스트로 반환
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
            result = self.read_modbus_value(
                address, self.meter_m_vol_mappings_value)
            # self.results를 self.read_results로 바꿀껀데 검증 필요함
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_vol_mappings_uint16.items():
            result = self.read_uint16(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_vol_mappings_uint32.items():
            result = self.read_uint32(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_value.items():
            result = self.read_modbus_value(
                address, self.meter_m_cur_mappings_value)
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
                print(f"Address {description}: Initial Value = {
                      initial}, Current Value = {current}")
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
    
    def reset_max_min(self):
        self.touch_manager.uitest_mode_start()
        addr_control_lock = 2901
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(ec.addr_reset_max_min.value, 1)
            print("Done")
        else:
            print(self.response.isError())
        self.reset_time = datetime.now()
        return self.reset_time


class Evaluation:

    reset_time = None
    ocr_manager = OCRManager()
    rois = config_data.roi_params()

    def __init__(self):
        self.labels = config_data.match_m_setup_labels()
        self.pop_params = config_data.match_pop_labels()
        self.m_home, self.m_setup = config_data.match_m_setup_labels()

    def eval_static_text(self, ocr_results_1, right_key):

        right_list = self.pop_params[right_key]
        ocr_right_1 = right_list

        right_list_1 = [text.strip() for text in ocr_right_1]
        ocr_list_1 = [result.strip() for result in ocr_results_1]

        leave_ocr_all = [
            result for result in ocr_list_1 if result not in right_list_1]
        leave_right_all = [
            text for text in right_list_1 if text not in ocr_list_1]

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

        leave_ocr_all = [
            result for result in ocr_list_1 if result not in right_list_1]
        leave_right_all = [
            text for text in right_list_1 if text not in ocr_list_1]

        ocr_error = leave_ocr_all
        right_error = leave_right_all

        # OCR 결과와 매칭되지 않아 남은 단어
        print(f"OCR 결과와 매칭되지 않는 단어들: {ocr_error}")
        print(f"\n정답 중 OCR 결과와 매칭되지 않는 단어들: {right_error}")

        return ocr_error, right_error

    def eval_demo_test(self, ocr_res, right_key, ocr_res_meas, image_path=None):
        self.meas_error = False
        self.condition_met = False
        color_data = config_data.color_detection_data()
        img_match_path = config_data.template_image_path()
        
        image = cv2.imread(image_path)

        ocr_right = self.m_home[right_key]

        right_list = ' '.join(text.strip() for text in ocr_right).split()
        ocr_rt_list = ' '.join(result.strip() for result in ocr_res).split()

        right_set = set(right_list)
        ocr_rt_set = set(ocr_rt_list)

        self.ocr_error = list(ocr_rt_set - right_set)
        right_error = list(right_set - ocr_rt_set)

        def check_results(values, limits, ocr_meas_subset):
            self.condition_met = True

            if isinstance(ocr_meas_subset, float):
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
                    
                elif numeric_value is not None and len(limits) >= 3 and isinstance(limits[0], (int, float)):
                    if limits[0] <= numeric_value < limits[1] and limits[2] == unit:
                        print(f"{name} = {numeric_value}{unit} (PASS)")
                    else:
                        print(f"{name} = {value} (FAIL)")
                        self.meas_error = True
                else:
                    print(f"{name} = {value} (FAIL)")
                    self.meas_error = True

        def img_match(image, roi_key, tpl_img_path):
            template_image_path = tpl_img_path[0]
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
        
        if "RMS Voltage" in ''.join(ocr_res[0]) or "Fund. Volt." in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, color_data["rms_voltage_L_L"]) <= 10:
                check_results(['AB', 'BC', 'CA', 'Aver'],
                              (180, 200, "V"), ocr_res_meas[:5])
            elif self.ocr_manager.color_detection(image, color_data["rms_voltage_L_N"]) <= 10:
                check_results(['A', 'B', 'C', 'Aver'],
                              (100, 120, "V"), ocr_res_meas[:5])
            else:
                print("demo test evaluation error")

        if self.ocr_manager.color_detection(image, color_data["mea_voltage"]) <= 10 and "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, color_data["vol_thd_L_L"]) <= 10:
                check_results(['AB', 'BC', 'CA'], (2.0, 4.0, "%"), ocr_res_meas[:4])
            elif self.ocr_manager.color_detection(image, color_data["vol_thd_L_N"]) <= 10:
                check_results(['A', 'B', 'C'], (3.0, 4.0, "%"),
                              ocr_res_meas[:4])
            else:
                print("demo test evaluation error")

        if "Frequency" in ''.join(ocr_res[0]):
            check_results(['Freq'], (59, 61, "Hz"), ocr_res_meas[:1])

        if "Residual Voltage" in ''.join(ocr_res[0]):
            check_results(["RMS", "Fund."], (0, 10, "V"), ocr_res_meas[:2])

        if "RMS Current" in ''.join(ocr_res[0]) or "Fundamental Current" in ''.join(ocr_res[0]):
            check_results(['A%', 'B%', 'C%', 'Aver%'], (45, 55, "%"), ocr_res_meas[:4])
            check_results(['A', 'B', 'C', 'Aver'], (2, 3, "A"), ocr_res_meas[4:])

        if self.ocr_manager.color_detection(image, color_data["mea_current"]) <= 10 and "Total Harmonic" in ''.join(ocr_res[0]):
            check_results(["A", "B", "C"], (0, 3.0, "%"), ocr_res_meas[:3])

        if "Total Demand" in ''.join(ocr_res[0]):
            check_results(["A", "B", "C"], (0, 1, "%"), ocr_res_meas[:3])

        if "Crest Factor" in ''.join(ocr_res[0]):
            check_results(["A", "B", "C"], (1.3, 1.6, ""), ocr_res_meas[:3])

        if "K-Factor" in ''.join(ocr_res[0]):
            check_results(["A", "B", "C"], (1.2, 1.5, ""), ocr_res_meas[:3])

        if "Residual Current" in ''.join(ocr_res[0]):
            check_results(["RMS"], (70, 100, "mA"), ocr_res_meas[:1])
            check_results(["RMS"], (20, 40, "mA"), ocr_res_meas[1:2])
            
        if "Active Power" in ''.join(ocr_res[0]):
            check_results(['A%', 'B%', 'C%', 'Total%'],(40, 50, "%"), ocr_res_meas[:4])
            check_results(["A", "B", "C"], (230, 240, "W"), ocr_res_meas[4:7])
            check_results(["Total"], (705, 715, "W"), ocr_res_meas[7:8])
            
        if "Reactive Power" in ''.join(ocr_res[0]):
            check_results(['A%', 'B%', 'C%', 'Total%'],(20, 30, "%"), ocr_res_meas[:4])
            check_results(["A", "B", "C"], (130, 145, "VAR"), ocr_res_meas[4:7])
            check_results(["Total"], (400, 420, "VAR"), ocr_res_meas[7:8])
            
        if "Apparent Power" in ''.join(ocr_res[0]):
            check_results(['A', 'B', 'C', 'Total'],(45, 55, "%"), ocr_res_meas[:4])
            check_results(["A", "B", "C"], (270, 280, "VA"), ocr_res_meas[4:7])
            check_results(["Total"], (810, 830, "VA"), ocr_res_meas[7:8])
            
        if "Power Factor" in ''.join(ocr_res[0]):
            check_results(['A%', 'B%', 'C%', 'Total%'],(45, 55, "Lag"), ocr_res_meas[:4])
            check_results(["A", "B", "C", "Total"], (0.860, 0.870, ""), ocr_res_meas[4:8])

        if "Phasor" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, color_data["phasor_VLL"]) <= 10:
                max_val= img_match(image_path, "phasor_img_cut", img_match_path[ec.phasor_vll])
                check_results(["AB", "BC", "CA"], (180, 200, "V" or "v"), ocr_res_meas[:3])
                check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6])
                check_results(["AB_angle"], (25, 35), ocr_res_meas[6:7])
                check_results(["BC_angle"], (-95, -85), ocr_res_meas[7:8])
                check_results(["CA_angle"], (145, 155), ocr_res_meas[8:9])
                check_results(["A_angle_cur"], (-35, -25), ocr_res_meas[9:10])
                check_results(["B_angle_cur"], (-155, -145), ocr_res_meas[10:11])
                check_results(["C_angle_cur"], (85, 95), ocr_res_meas[11:12])
                check_results(["Phasor_image"], (0.98, 1), max_val)
            elif self.ocr_manager.color_detection(image, color_data["phasor_VLN"]) <= 10:
                max_val= img_match(image_path, "phasor_img_cut", img_match_path[ec.phasor_vll])
                check_results(["A", "B", "C"], (100, 120, "V" or "v"), ocr_res_meas[:3])
                check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6])
                check_results(["A_angle"], (0, 5), ocr_res_meas[6:7])
                check_results(["B_angle"], (-125, -115), ocr_res_meas[7:8])
                check_results(["C_angle"], (115, 125), ocr_res_meas[8:9])
                check_results(["A_angle_cur"], (-35, -25), ocr_res_meas[9:10])
                check_results(["B_angle_cur"], (-155, -145), ocr_res_meas[10:11])
                check_results(["C_angle_cur"], (85, 95), ocr_res_meas[11:12])
            else:
                print("demo test evaluation error")

        if "Harmonics" in ''.join(ocr_res[0]):
            check_results(["A_THD", "B_THD", "C_THD"], (3.0, 4.0, "%"), ocr_res_meas[:3])
            check_results(["A_Fund", "B_Fund", "C_Fund"], (100, 120, "V" or "v"), ocr_res_meas[3:6])
        
        if "Waveform" in ''.join(ocr_res[0]):
            pass    
        
        if "Volt. Symm. Component" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, color_data["vol_thd_L_L"]) <= 10:
                check_results(['V1', 'V2'], (180, 200, "V" or "v"), ocr_res_meas[2:3])
                check_results(['V1', 'V2'], (0, 1, "V" or "v"), ocr_res_meas[3:4])
            elif self.ocr_manager.color_detection(image, color_data["vol_thd_L_N"]) <= 10:
                check_results(['V1', 'V2'], (100, 110, "V" or "v"), ocr_res_meas[2:3])
                check_results(['V1', 'V2'], (0, 1, "V" or "v"), ocr_res_meas[3:4])
                
        if "Voltage Unbalance" in ''.join(ocr_res[0]):
            check_results(['NEMA LL', 'NEMA LN', "U2", "U0"], (0, 1, "%"), ocr_res_meas[0:4])
            check_results(['NEMA LL', 'NEMA LN', "U2", "U0"], (0, 1, "%"), ocr_res_meas[4:8])
            
        if "Curr. Symm. Component" in ''.join(ocr_res[0]):
            check_results(["I1"], (0, 1, "l1"), ocr_res_meas[0:1])
            check_results(["I1"], (0, 1, "l2"), ocr_res_meas[1:2])
            check_results(["I1"], (0, 1, "l0"), ocr_res_meas[2:3])
            check_results(["I1", "I2", "I0"], (2, 3), ocr_res_meas[3:4])
            check_results(["I1", "I2", "I0"], (0, 0.1), ocr_res_meas[4:5])
            check_results(["I1", "I2", "I0"], (0, 0.1), ocr_res_meas[5:6])
            
        if "Current Unbalance" in ''.join(ocr_res[0]):
            check_results([""], (0, 1, "empty"), ocr_res_meas[0:1])
            check_results(["U2"], (0, 1, "U2"), ocr_res_meas[1:2])
            check_results(["U0"], (0, 1, "U0"), ocr_res_meas[2:3])
            check_results(["", "U2", "U0"], (0, 1, "%"), ocr_res_meas[3:6])

        if not self.condition_met:
            print("Nothing matching word")

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")

        return self.ocr_error, right_error, self.meas_error, ocr_res

    def check_time_diff(self, time_images, reset_time):
        if not reset_time:
            reset_time = datetime.now()

        time_format = "%Y-%m-%d %H:%M:%S"
        results = []
        for time_str in time_images:
            try:
                image_time = datetime.strptime(time_str, time_format)
                time_diff = abs(
                    (image_time - reset_time).total_seconds())
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

    def save_csv(self, ocr_img, ocr_error, right_error, meas_error=False, ocr_img_meas=None, ocr_img_time=None, time_results=None, img_path=None):
        ocr_img_meas = ocr_img_meas if ocr_img_meas is not None else []
        ocr_img_time = ocr_img_time if ocr_img_time is not None else []
        time_results = time_results if time_results is not None else []

        num_entries = max(len(ocr_img), len(ocr_img_meas), len(ocr_img_time))

        overall_result = "PASS"
        if ocr_error or right_error or meas_error:
            overall_result = "FAIL"
        if any("FAIL" in result for result in time_results):
            overall_result = "FAIL"

        csv_results = {
            "Main View": ocr_img + [None] * (num_entries - len(ocr_img)),
            "Measurement": ocr_img_meas + [None] * (num_entries - len(ocr_img_meas)),
            "OCR-Right": [f"{ocr_error} ({overall_result})"] * num_entries,
            "Right-OCR": [f"{right_error} ({overall_result})"] * num_entries,
            f"Time Stemp ({self.reset_time})": time_results + [None] * (num_entries - len(time_results)),
        }

        df = pd.DataFrame(csv_results)
        
        file_name_with_extension = os.path.basename(img_path)
        ip_to_remove = "10.10.26.159_"
        if file_name_with_extension.startswith(ip_to_remove):
            file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
        else:
            file_name_without_ip = file_name_with_extension

        image_file_name = os.path.splitext(file_name_without_ip)[0]
        
        save_path = os.path.expanduser(f"./csvtest/{overall_result}_ocr_{image_file_name}.csv")

        df.to_csv(save_path, index=False)
        dest_image_path = os.path.join(os.path.dirname(save_path), file_name_without_ip)
        shutil.copy(img_path, dest_image_path)
