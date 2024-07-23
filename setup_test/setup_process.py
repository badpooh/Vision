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

    def ST_measurement(self):
        self.touch_manager.menu_touch("main_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_1")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path, "measurement", "mea_voltage", self.image_uitest.label_voltage)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_2")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path1 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path1, "measurement", "mea_current", self.image_uitest.label_current)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_3")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path2 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path2, "measurement", "mea_demand", self.image_uitest.label_demand)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_4")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path3 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path3, "measurement", "mea_power", self.image_uitest.label_power)

    def PT_measurement(self):
        self.touch_manager.menu_touch("main_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("data_view_2")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        self.touch_manager.menu_touch("btn_cancel")
        time.sleep(0.6)
        image_path = self.load_image_file()
        roi_keys = ["20", "21"]
        select_ocr = "2"
        self.static_popup_text(image_path, select_ocr, roi_keys)

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
    
    def static_text_measurement(self, image_path, color1, color2, select_ocr, roi_keys):       
        test_image_path = image_path
        image = cv2.imread(test_image_path)
        color_result = self.edit_image.color_detection(image, *self.coords_color[color1])
        color_result1 = self.edit_image.color_detection(image, *self.coords_color[color2])

        if color_result < 5 and color_result1 < 5:
            roi_keys = ["1", "2", "5", "6", "9", "10", "13", "14"]
            cutted_image = self.edit_image.image_cut_custom(image=test_image_path, roi_keys=roi_keys)
            select_ocr = ["1"]
            ocr_error, right_error = self.image_uitest.eval_static_text(cutted_image, select_ocr)
            if not ocr_error and not right_error:
                print("PASS")
            else:
                print("FAIL: different text")
        else:
            print("FAIL: different menu")
            
    def static_popup_text(self, image_path, select_ocr, roi_keys):       
        test_image_path = image_path
        cutted_image = self.edit_image.image_cut_custom(image=test_image_path, roi_keys=roi_keys)
        ocr_error, right_error = self.image_uitest.eval_static_text(cutted_image, select_ocr)
        if not ocr_error and not right_error:
            print("PASS")
        else:
            print("FAIL: different text")
        return 
            
    def variable_text(self, image_path, select_ocr, roi_keys):       
        test_image_path = image_path
        
        # 첫 번째 이미지 처리
        cutted_images = self.edit_image.image_cut_custom(image=test_image_path, roi_keys=roi_keys)
        
        # 두 번째 이미지 처리
        roi_key = ["main_view_4", "main_view_8", "main_view_12", "main_view_16"]
        ocr_calcul_results = self.edit_image.image_cut_custom(image=test_image_path, roi_keys=roi_key)
        
        # OCR 결과 비교
        ocr_error, right_error = self.image_uitest.eval_demo_test(cutted_images, select_ocr, ocr_calcul_results)
        
        if not ocr_error and not right_error:
            print("PASS")
        else:
            print("FAIL: different text")
             
    def mea_demo_mode(self):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_setup()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.menu_touch("data_view_2")
        self.touch_manager.screenshot()
        image_path = self.load_image_file()
        roi_keys = ["999"]
        cutted_image = self.edit_image.image_cut_custom(image=image_path, roi_keys=roi_keys)
        if "Password" in cutted_image:
            for _ in range(4): 
                self.touch_manager.menu_touch("btn_num_pw_0")
            self.touch_manager.menu_touch("btn_num_pw_enter")
            self.touch_manager.menu_touch("infinite")
            self.touch_manager.menu_touch("btn_popup_enter")
            self.touch_manager.menu_touch("btn_apply")
        else:
            print("error")
            self.touch_manager.menu_touch("btn_popup_cencel")
        self.touch_manager.menu_touch("data_view_1")
        self.touch_manager.menu_touch("btn_testmode_2")
        self.touch_manager.menu_touch("btn_popup_enter")
        self.touch_manager.menu_touch("btn_apply")
        print("Demo Mode Start")

            
    def testcode01(self):
        image_path = r"C:\PNT\09.AutoProgram\AutoProgram\image_test\vol_max2.png"
        time.sleep(1)
        roi_keys = ["main_view_1", "main_view_2", "main_view_3", "main_view_5"]
        select_ocr = "RMS"
        self.variable_text(image_path, select_ocr, roi_keys)
        time.sleep(0.6)
        ## popup 화면 설정값 범위 및 고정 텍스트 읽는거 추가