import cv2
import numpy as np
import os, glob
from datetime import datetime
import time

from setup_test.setup_function import TouchManager, ModbusManager, OCRManager, Evaluation, ModbusLabels


image_directory = r"\\10.10.20.30\screenshot"


class SetupProcess:
    
    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    ocr_func = OCRManager()
    evaluation = Evaluation()
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
        self.static_text_measurement(image_path, "measurement", "mea_voltage", self.evaluation.label_voltage)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_2")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path1 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path1, "measurement", "mea_current", self.evaluation.label_current)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_3")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path2 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path2, "measurement", "mea_demand", self.evaluation.label_demand)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_4")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path3 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(image_path3, "measurement", "mea_power", self.evaluation.label_power)

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
        color_result = self.ocr_func.color_detection(image, *self.coords_color[color1])
        color_result1 = self.ocr_func.color_detection(image, *self.coords_color[color2])

        if color_result < 5 and color_result1 < 5:
            roi_keys = ["1", "2", "5", "6", "9", "10", "13", "14"]
            cutted_image = self.ocr_func.ocr_basic(image=test_image_path, roi_keys=roi_keys)
            select_ocr = ["1"]
            ocr_error, right_error = self.evaluation.eval_static_text(cutted_image, select_ocr)
            if not ocr_error and not right_error:
                print("PASS")
            else:
                print("FAIL: different text")
        else:
            print("FAIL: different menu")
            
    def static_popup_text(self, image_path, select_ocr, roi_keys):       
        test_image_path = image_path
        cutted_image = self.ocr_func.ocr_basic(image=test_image_path, roi_keys=roi_keys)
        ocr_error, right_error = self.evaluation.eval_static_text(cutted_image, select_ocr)
        if not ocr_error and not right_error:
            print("PASS")
        else:
            print("FAIL: different text")
        return 
            
    def variable_text(self, image_path, select_ocr, roi_keys, roi_key):       
        test_image_path = image_path
        
        # 첫 번째 이미지 처리
        cutted_images = self.ocr_func.ocr_basic(image=test_image_path, roi_keys=roi_keys)
        
        # 두 번째 이미지 처리
        ocr_calcul_results = self.ocr_func.ocr_basic(image=test_image_path, roi_keys=roi_key)
        
        # OCR 결과 비교
        ocr_error, right_error = self.evaluation.eval_demo_test(cutted_images, select_ocr, ocr_calcul_results)
        
        if not ocr_error and not right_error:
            print("PASS")
        else:
            print("FAIL: different text")
            
    def ocr_process(self, image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys=None):
            """
            Args:
                image_path (str): The path to the image file.
                roi_keys (list): List of ROI keys for general OCR processing.
                roi_keys_meas (list): List of ROI keys for measurement OCR processing.
                ocr_ref (str): The OCR type to be selected for evaluation.
                time_keys (list): Min, Max time
            Returns:
                None
            """
            ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
            ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
            if time_keys is not None:
                ocr_img_time = self.ocr_func.ocr_basic(image=image_path, roi_keys=time_keys)
                time_error = self.evaluation.check_time_diff(ocr_img_time)
                ocr_error, right_error, meas_error = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
                self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, ocr_img_time, time_error)
            else:
                ocr_error, right_error, meas_error = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
                self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas)
                
    def ocr_4phase(self, ref): ### A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["a_meas", "b_meas", "c_meas", "aver_meas"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
    
    def ocr_curr_4phase(self, image_path, ref): ### A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        # image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3", "cur_percent_4", "a_meas", "b_meas", "c_meas", "aver_meas"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
                
    def ocr_4phase_time(self, ref): ### A,B,C,Aver + time stamp ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["a_meas", "b_meas", "c_meas", "aver_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp", "c_time_stamp", "aver_time_stamp"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
    def ocr_curr_4phase_time(self, image_path, ref): ### A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        # image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3", "cur_percent_4", "a_meas", "b_meas", "c_meas", "aver_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp", "c_time_stamp", "aver_time_stamp"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
    def ocr_3phase(self, ref): ### A,B,C ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["a_meas", "b_meas", "c_meas"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
        
    def ocr_3phase_time(self, ref): ### A,B,C + time stamp ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["a_meas", "b_meas", "c_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp", "c_time_stamp"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)

class DemoTest:

    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    ocr_func = OCRManager()
    evaluation = Evaluation()
    modbus_label = ModbusLabels()
    sp = SetupProcess()
    search_pattern = os.path.join(image_directory, './**/*10.10.26.156*.png')
    now = datetime.now()
    file_time_diff = {}

    def mea_demo_mode(self):
        ### Timeout을 infinite로 변경 후 Test Mode > Balance로 실행 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_setup()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.menu_touch("data_view_2")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["999"]
        cutted_image = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
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

    def reset_max_min(self):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_setup()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.menu_touch("data_view_3")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["999"]
        cutted_image = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        if "Password" in cutted_image:
            for _ in range(4): 
                self.touch_manager.menu_touch("btn_num_pw_0")
            self.touch_manager.menu_touch("btn_num_pw_enter")
            self.touch_manager.menu_touch("cauiton_confirm")
            self.touch_manager.menu_touch("btn_apply")
        else:
            print("error")
            self.touch_manager.menu_touch("btn_popup_cencel")
        self.MM_clear_time = datetime.now
        print(self.MM_clear_time)

    def demo_mea_vol_rms(self):
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.menu_touch("meas_L-L")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("rms_vol_L_L")
        
        ### L-L min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_L")
        
        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_L")
        
        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N")
        
         ### L-N min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N")
        
        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N")

    def demo_mea_vol_fund(self):
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.menu_touch("meas_L-L")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("fund_vol_L_L")
        
        ### L-L min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_L")
        
        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_L")
        
        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("fund_vol_L_N")
        
         ### L-N min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_N")
        
        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_N")

        print("Voltage_RMS_Done")
    
    def demo_mea_vol_thd(self): 
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.menu_touch("thd_L-L")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("thd_vol_L_L")
        
        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("thd_vol_L_L")
        
        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("thd_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("thd_vol_L_N")

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("thd_vol_L_N")
        
    def demo_mea_vol_freq(self):
        ### 기본주파수 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = ["freq"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
        
        ### 주파수 Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = ["freq"]
        time_keys = ["a_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
        ### 주파수 Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = ["freq"]
        time_keys = ["a_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
    def demo_mea_vol_residual(self):
        ### 기본 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_5")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = ["vol_residual"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
        
        ### 잔류전압 Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = ["vol_residual"]
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
        ### 잔류전압 Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = ["vol_residual"]
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
    def demo_mea_curr_rms(self):
        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("rms_curr")

        ### Current Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr")
        
        ### Current Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr")
        
    def demo_mea_curr_fund(self):
        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("rms_curr")

        ### Current Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr")
        
        ### Current Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr")
        
    def demo_mea_curr_thd(self):
        ### Current thd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_thd")

        ### Current thd Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_thd")
        
    def demo_mea_curr_tdd(self):
        ### Current tdd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_5")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_tdd")

        ### Current tdd Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_tdd")
        
    def demo_mea_curr_cf(self):
        ### Current crest factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_6")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_cf")
        
        ### Current crest factor Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_cf")
        
    def demo_mea_curr_kf(self):
        ### Current k-factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_7")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_kf")

        ### Current k-factor Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_kf")
        
    def demo_mea_curr_residual(self):
        ### Current residual ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_8")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = ["curr_residual"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
        
        ### Current residual Min###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = ["curr_residual"]
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
    
    def demo_mea_anal_phasor(self):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_1")

        
    def testcode01(self):
        image_path = r"C:\Users\Jin\Desktop\Company\Rootech\PNT\AutoProgram\image_test\10.10.26.156_2024-08-09_09_48_40_M_H_CU_RMS.png"
        time.sleep(1)
        self.sp.ocr_curr_4phase(image_path, "rms_curr")
        
    def testcode02(self):
        # self.modbus_label.demo_test_setting()
        # self.reset_max_min()
        self.demo_mea_vol_rms()
        # self.demo_mea_vol_fund()
        # self.demo_mea_vol_thd()
        # self.demo_mea_curr_rms()
        pass

    def testcode03(self):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["main_view_1", "main_view_2", "main_view_5", "main_view_6", "main_view_9", "main_view_10", "main_view_13", "main_view_14", "main_view_17"]
        roi_keys_meas = ["main_view_4", "main_view_8", "main_view_12", "main_view_16"]
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        select_ocr = "rms_vol_L-N"
        ocr_error, right_error, meas_error = self.evaluation.eval_demo_test(ocr_img, select_ocr, ocr_img_meas)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas,)