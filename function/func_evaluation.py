import re
import numpy as np
import cv2
from datetime import datetime, timezone
import shutil
import os
import glob
import pandas as pd
from collections import Counter

from function.func_ocr import OCRManager
from function.func_connection import ConnectionManager

from config.config_roi import Configs
from config.config_color import ConfigColor as cc
from config.config_ref import ConfigImgRef as cr
from config.config_map import ConfigModbusMap as ecm
from config.config_map import ConfigInitialValue as civ

class Evaluation:

    reset_time = None
    ocr_manager = OCRManager()
    config_data = Configs()
    rois = config_data.roi_params()
    connect_manager = ConnectionManager()

    def __init__(self):
        pass

    def load_image_file(self, search_pattern):
        self.now = datetime.now()
        self.file_time_diff = {}

        for file_path in glob.glob(search_pattern, recursive=True):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            time_diff = abs((self.now - creation_time).total_seconds())
            self.file_time_diff[file_path] = time_diff

        closest_file = min(self.file_time_diff,
                            key=self.file_time_diff.get, default=None)
        normalized_path = os.path.normpath(closest_file)
        self.latest_image_path = normalized_path

        print("가장 가까운 시간에 생성된 파일:", normalized_path)

        return self.latest_image_path

    ### With Demo Balance ###
    def eval_demo_test(self, ocr_res, right_key, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        
        image = cv2.imread(image_path)

        ocr_right = right_key

        right_list = ' '.join(text.strip() for text in ocr_right).split()
        ocr_rt_list = ' '.join(result.strip() for result in ocr_res).split()

        right_counter = Counter(right_list)
        ocr_rt_counter = Counter(ocr_rt_list)

        self.ocr_error = list((ocr_rt_counter - right_counter).elements())
        right_error = list((right_counter - ocr_rt_counter).elements())

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
            if self.ocr_manager.color_detection(image, cc.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (180, 200, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, cc.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (100, 120, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, cc.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (2.0, 4.0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, cc.color_vol_thd_ln.value) <= 10:
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
            if self.ocr_manager.color_detection(image, cc.color_main_menu_curr.value) <= 10: 
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
            if self.ocr_manager.color_detection(image, cc.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (180, 195, "V" or "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (25, 35, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (-95, -85, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (145, 155, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vll.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, cc.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (100, 120, "V" or "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (-0.2, 5, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (-125, -115, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (115, 125, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vln.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_harmonics_vol.value) <= 10:
                if img_result == 1 or img_result == 0:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (0.9, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (2, 5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v" or "V"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.95, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (2, 5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v" or "V"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    all_meas_results.extend("PASS?")
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (3.0, 4.0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
            else:
                if img_result == 1 or img_result == 0:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (1, 1, ""), img_result))  
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.95, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (2, 5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v" or "V"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
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
            if self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (180, 200, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (180, 200, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (180, 200, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 1, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ll.value) <= 10:
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
            
        elif "Demand Currnet" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A%", "B%", "C%", "Aver%"], (40, 60, "%"), ocr_res_meas[0:5]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (4, 6, "A"), ocr_res_meas[5:9]))
        
        elif not self.condition_met:
            print("Nothing matching word")

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")

        return self.ocr_error, right_error, self.meas_error, ocr_res, all_meas_results,

    ### No source, No Demo ###
    def eval_none_test(self, ocr_res, right_key, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        
        image = cv2.imread(image_path)

        right_list = ' '.join(text.strip() for text in right_key).split()
        ocr_rt_list = ' '.join(result.strip() for result in ocr_res).split()

        right_counter = Counter(right_list)
        ocr_rt_counter = Counter(ocr_rt_list)

        self.ocr_error = list((ocr_rt_counter - right_counter).elements())
        right_error = list((right_counter - ocr_rt_counter).elements())

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
            if self.ocr_manager.color_detection(image, cc.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (0, 0, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, cc.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, cc.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (0, 0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, cc.color_vol_thd_ln.value) <= 10:
                    all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "%"), ocr_res_meas[:4]))
                else:
                    print("Total Harmonic missed")

        elif "Frequency" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["Freq"], (0, 0, "Hz"), ocr_res_meas[:1]))

        elif "Residual Voltage" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS", "Fund."], (0, 0, "V"), ocr_res_meas[:2]))

        elif "RMS Current" in ''.join(ocr_res[0]) or "Fundamental Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Aver %"], (0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "A"), ocr_res_meas[4:]))

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_main_menu_curr.value) <= 10: 
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "%"), ocr_res_meas[:3]))

        elif "Total Demand" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "%"), ocr_res_meas[:3]))

        elif "Crest Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, ""), ocr_res_meas[:3]))

        elif "K-Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, ""), ocr_res_meas[:3]))

        elif "Residual Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS"], (0, 0, "A"), ocr_res_meas[:1]))
            all_meas_results.extend(check_results(["RMS"], (0, 0, "A"), ocr_res_meas[1:2]))
            
        elif "Active Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Total %"], (0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "kW"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (0, 0, "kW"), ocr_res_meas[7:8]))
            
        elif "Reactive Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "kVAR"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (0, 0, "kVAR"), ocr_res_meas[7:8]))
            
        elif "Apparent Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A', 'B', 'C', 'Total'],(0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "kVA"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (0, 0, "kVA"), ocr_res_meas[7:8]))
            
        elif "Power Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(0, 0, "No Load"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Total"], (1, 1, ""), ocr_res_meas[4:8]))
            
        elif "Phasor" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (0, 0, "V"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (0, 0, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (0, 0, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (0, 0, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (0, 0, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (0, 0, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (0, 0, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (0, 0, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vll_none.value], (0.99, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, cc.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "V"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (0, 0, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (0, 0, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (0, 0, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (0, 0, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (0, 0, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (0, 0, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (0, 0, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vln_none.value], (0.99, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_harmonics_vol.value) <= 10:
                if img_result is not None:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (0.9, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (0, 0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (0, 0, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.9, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (0, 0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (0, 0, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    print(ocr_res_meas)
                    all_meas_results.extend(check_results(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], (0, 0, ""), ocr_res_meas[0:10]))
                    print("test")
            else:
                if img_result is not None:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (0.9, 1, ""), img_result))  
                    # all_meas_results.extend(check_results(["CURR_A_THD", "CURR_B_THD", "CURR_C_THD"], (0, 0, "%"), ocr_res_meas[:3]))
                    # all_meas_results.extend(check_results(["CURR_A_Fund", "CURR_B_Fund", "CURR_C_Fund"], (0, 0, "A"), ocr_res_meas[3:6]))
                    # all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.9, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    all_meas_results.extend("PASS?")
            
                    
        elif "Waveform" in ''.join(ocr_res[0]):
            if 0 < img_result < 1:
                all_meas_results.extend(check_results(["waveform_image"], (0.945, 1, ""), img_result))
            else:
                all_meas_results.extend(check_results(["waveform_img_detect"], (1, 1, ""), img_result))
                
        elif "Volt. Symm. Component" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (0, 0, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (0, 0, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (0, 0, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V0'], (0, 0, "V0"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V1'], (0, 0, "V" or "v"), ocr_res_meas[3:4]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V" or "v"), ocr_res_meas[4:5]))
                all_meas_results.extend(check_results(['V0'], (0, 0, "V" or "v"), ocr_res_meas[5:6]))
                
        elif "Voltage Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["NEMA LL"], (0, 0, "LL"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["NEMA LN"], (0, 0, "LN"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U2"], (0, 0, "U2"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["U0"], (0, 0, "U0"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["NEMA LL", "NEMA LN", "U2", "U0"], (0, 1, "%"), ocr_res_meas[4:8]))
            
        elif "Curr. Symm. Component" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["I1"], (0, 0, "l1"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["I2"], (0, 0, "l2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["I0"], (0, 0, "l0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["I1"], (0, 0, "A"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["I2"], (0, 0, "A"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["I0"], (0, 0, "A"), ocr_res_meas[5:6]))
            
        elif "Current Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results([""], (0, 0, "empty"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["U2"], (0, 0, "U2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U0"], (0, 0, "U0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results([""], (0, 0, "%"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["U2"], (0, 0, "%"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["U0"], (0, 0, "%"), ocr_res_meas[5:6]))
        
        elif "Demand Currnet" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A%", "B%", "C%", "Aver%"], (0, 0, "%"), ocr_res_meas[0:5]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "A"), ocr_res_meas[5:9]))
            
        elif not self.condition_met:
            print("Nothing matching word")

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")

        return self.ocr_error, right_error, self.meas_error, ocr_res, all_meas_results
    
    def eval_setup_test(self, ocr_res, setup_ref,sm_res=None, except_addr=None):
        """
        ocr_res: OCR 결과 리스트
        sm_res:  AccurSM 결과
        except_addr: 검사에서 제외해야 할 ConfigModbusMap 멤버의 집합 (예: {ConfigModbusMap.addr_wiring, ...})
        """

        if except_addr is None:
            except_addr = set()

        ocr_list = ' '.join(result.strip() for result in ocr_res).split()

        if "Wiring" in ''.join(ocr_list[0]):
            self.connect_manager.setup_client.read_holding_registers(*ecm.addr_measurement_setup_access.value)
            current_wiring = self.connect_manager.setup_client.read_holding_registers(*ecm.addr_wiring.value)
            if setup_ref == "Wye":
                if ocr_list[1] == "Wye":
                    if current_wiring.registers[0] == 0:
                        setup_result = ['PASS', f'Device = {ocr_list[1]}', f'Modbus = {current_wiring.registers[0]}', "AccuraSM = Wye"]
                    else:
                        setup_result = ['FAIL', "Wiring modbus error"]
                else:
                    setup_result = ['FAIL', "Wiring device UI error"]
            if setup_ref == "Delta":
                if ocr_list[1] == "Delta":
                    if current_wiring.registers[0] == 1:
                        setup_result = ['PASS', f'Device = {ocr_list[1]}', f'Modbus = {current_wiring.registers[0]}', "AccuraSM = Wye"]
                    else:
                        setup_result = ['FAIL', "Wiring modbus error"]
                else:
                    setup_result = ['FAIL', "Wiring device UI error"]
        else:
            setup_result = ['FAIL', "Unknown first part"]

        evaluation_results = {}

        for modbus_enum, expected in civ.initial_setup_values.value.items():
            if modbus_enum in except_addr:
                continue

            address, words = modbus_enum.value
            response = self.connect_manager.setup_client.read_holding_registers(address, words)

            if words is None:
                continue
            elif words == 1:
                current_value = response.registers[0]
            elif words == 2:
                high = response.registers[0]
                low = response.registers[1]
                current_value = (high << 16) | low
            else:
                current_value = None
            
            if expected is not None and current_value != expected:
                evaluation_results[modbus_enum] = {
                    "expected": expected,
                    "current": current_value
                }

        if evaluation_results:
            print("변경되지 말아야 할 레지스터 중 차이가 발견되었습니다:")
            for addr_enum, diff in evaluation_results.items():
                modbus_results = f"FAIL, 주소 {addr_enum.value}: 예상 {diff['expected']}, 실제 {diff['current']}"
                print(f"주소 {addr_enum.value}: 예상 {diff['expected']}, 실제 {diff['current']}")
        else:
            modbus_results = 'PASS'
            print("모든 변경되지 말아야 할 레지스터가 정상입니다.")
        
        return setup_result, modbus_results

    
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
            csv_result = f"{target_color} FAIL"
        else:
            print(f"{target_color} (PASS)")
            result = 1
            csv_result = f"{target_color} PASS"
        return result, csv_result

    def check_time_diff(self, image, roi_keys, reset_time, test_mode):
        self.reset_time = reset_time
        if not self.reset_time:
            self.reset_time = datetime.now()

        ocr_results_time = self.ocr_manager.ocr_basic(image, roi_keys)

         # 유효한 텍스트만 리스트로 반환
        time_images = [text for text in ocr_results_time if text]

        time_format = "%Y-%m-%d %H:%M:%S"
        time_results = []
        for time_str in time_images:
            try:
                image_time = datetime.strptime(time_str, time_format)
                image_time = image_time.replace(tzinfo=timezone.utc)
                time_diff = abs((image_time - self.reset_time).total_seconds())
                if test_mode == "Demo":
                    if time_diff <= 120:
                        print(f"{time_str} (PASS)")
                        time_results.append(f"{time_str} (PASS)")
                    else:
                        print(f"{time_str} / {time_diff} seconds (FAIL)")
                        time_results.append(f"{time_str} / {time_diff} seconds (FAIL)")
                else:
                    if time_diff <= 5:
                        print(f"{time_str} (PASS)")
                        time_results.append(f"{time_str} (PASS)")
                    else:
                        print(f"{time_str} / {time_diff} seconds (FAIL)")
                        time_results.append(f"{time_str} / {time_diff} seconds (FAIL)")
            except ValueError as e:
                print(f"Time format error for {time_str}: {e}")
                time_results.append(f"{time_str} / format error (FAIL)")
        return time_results

    def save_csv(self, ocr_img, ocr_error, right_error, meas_error=False, ocr_img_meas=None, ocr_img_time=None, time_results=None, img_path=None, img_result=None, base_save_path=None, all_meas_results=None, invalid_elements=None):
        ocr_img_meas = ocr_img_meas if ocr_img_meas is not None else []
        # ocr_img_time = ocr_img_time if ocr_img_time is not None else []
        time_results = time_results if time_results is not None else []
        img_result = [img_result]

        if invalid_elements is None:
            invalid_elements = []

        if ocr_img_meas == bool:
            ocr_img_meas = []
            num_entries = max(len(ocr_img), len(ocr_img_meas)+1, len(time_results)+1, len(img_result)+1)
        else:
            num_entries = max(len(ocr_img), len(ocr_img_meas)+1, len(time_results)+1, len(img_result)+1)

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
            f"Time Stamp ({self.reset_time})": [None] + time_results + [None] * (num_entries - len(time_results)-1),
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
        ip_to_remove = f"{self.connect_manager.SERVER_IP}_"
        if file_name_with_extension.startswith(ip_to_remove):
            file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
        else:
            file_name_without_ip = file_name_with_extension

        image_file_name = os.path.splitext(file_name_without_ip)[0]
        
        save_path = os.path.join(base_save_path, f"{overall_result}_ocr_{image_file_name}.csv")

        df.to_csv(save_path, index=False)
        dest_image_path = os.path.join(base_save_path, file_name_without_ip)
        shutil.copy(img_path, dest_image_path)

    def count_csv_and_failures(self, folder_path, start_time, end_time):
        end_file = '.csv'
        csv_files = [f for f in os.listdir(folder_path) if f.endswith(end_file)]

        total_csv_files = 0
        fail_count = 0

        for file_name in csv_files:
            try:
                parts = file_name.split('_')
                # 날짜와 시간 부분 추출
                date_part = parts[2]  # '2025-01-22'
                time_part = "_".join(parts[3:6])  # '17_08_41'
                file_time_str = f"{date_part}_{time_part}"  # '2025-01-22_17_08_41'
                file_time = datetime.strptime(file_time_str, "%Y-%m-%d_%H_%M_%S")

                # start_time과 end_time의 타임존 정보 제거
                start_time_naive = start_time.replace(tzinfo=None)
                end_time_naive = end_time.replace(tzinfo=None)

                # 시간 범위 체크
                if start_time_naive <= file_time <= end_time_naive:
                    total_csv_files += 1
                    if 'FAIL' in file_name.upper():
                        fail_count += 1

            except (IndexError, ValueError):
                print(f"[DEBUG] 파일 이름 분리 결과: {file_name.split('_')}")
                print(f"[WARN] 파일 이름에서 시간을 추출할 수 없습니다: {file_name}")

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