import cv2
import numpy as np
import os, glob
from datetime import datetime
import time

from setup_test.setup_function import TouchManager, ModbusManager, OCRImageManager, Evaluation, ModbusLabels


image_directory = r"\\10.10.20.30\screenshot"


class SetupProcess:
    
    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    edit_image = OCRImageManager()
    image_uitest = Evaluation()
    modbus_label = ModbusLabels()
    search_pattern = os.path.join(image_directory, './**/*10.10.26.156*.png')
    now = datetime.now()
    file_time_diff = {}

    def __init__(self):
        self.coords_touch = self.touch_manager.coords_touch
        self.coords_color = self.touch_manager.coords_color
        self.coords_TA = self.touch_manager.coords_TA

    def modbus_connect(self):
        self.modbus_manager.start_monitoring()

    def modbus_discon(self):
        self.modbus_manager.tcp_disconnect()

    def FT_measurement(self):
        self.touch_manager.menu_touch("main_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_1")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path = self.load_image_file()
        time.sleep(1)
        self.fixed_text_measurement(image_path, "measurement", "mea_voltage", self.image_uitest.label_voltage)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_2")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path1 = self.load_image_file()
        time.sleep(1)
        self.fixed_text_measurement(image_path1, "measurement", "mea_current", self.image_uitest.label_current)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_3")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path2 = self.load_image_file()
        time.sleep(1)
        self.fixed_text_measurement(image_path2, "measurement", "mea_demand", self.image_uitest.label_demand)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_4")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path3 = self.load_image_file()
        time.sleep(1)
        self.fixed_text_measurement(image_path3, "measurement", "mea_power", self.image_uitest.label_power)
    
    def load_image_file(self):
        self.now = datetime.now()
        self.file_time_diff = {}

        for file_path in glob.glob(self.search_pattern, recursive=True):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            time_diff = abs((self.now - creation_time).total_seconds())
            self.file_time_diff[file_path] = time_diff

        closest_file = min(self.file_time_diff, key=self.file_time_diff.get, default=None)
        normalized_path = os.path.normpath(closest_file)

        print("가장 가까운 시간에 생성된 파일:", normalized_path)

        return normalized_path

    def read_setup_mapping(self):
        modbus_results = self.modbus_label.read_all_modbus_values()
        for description, value in modbus_results.items():
            print(f"{description}: {value}")
    
    def fixed_text_measurement(self, image_path, color1, color2, select_ocr):       
        test_image_path = image_path
        image = cv2.imread(test_image_path)
        color_result = self.edit_image.color_detection(image, *self.coords_color[color1])
        color_result1 = self.edit_image.color_detection(image, *self.coords_color[color2])

        if color_result < 5 and color_result1 < 5:
            roi_keys = ["1", "2", "5", "6", "9", "10", "13", "14"]
            cutted_image = self.edit_image.image_cut_custom(image=test_image_path, roi_keys=roi_keys)
            ocr_error, right_error = self.image_uitest.evaluation_ocr(cutted_image, select_ocr)
            if not ocr_error and not right_error:
                print("PASS")
            else:
                print("FAIL: different text")
        else:
            print("FAIL: different menu")
             
        #### 3P4W일때 Wiring 제외하고 모든 설정 ####
    def test_m_m_v(self):
        initial_values = self.modbus_label.read_all_modbus_values()
        time.sleep(1)
        self.touch_manager.menu_touch("main_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("data_view_2")
        time.sleep(0.6)
        #### 최소치 1 ####
        self.touch_manager.number_1_touch("btn_number_1")
        time.sleep(0.6)
        change_count = self.modbus_label.display_changes(initial_values)
        if change_count >= 2:
            print("check other address value")
        else:
            self.touch_manager.screenshot()
            time.sleep(0.6)
            image_path = self.load_image_file()
            self.fixed_text_measurement(image_path)