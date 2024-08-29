import cv2
import numpy as np
import os
import glob
from datetime import datetime
import time
import re

from setup_test.setup_function import TouchManager, ModbusManager, OCRManager, Evaluation, ModbusLabels
from setup_test.setup_config import ConfigTextRef as ec
from setup_test.setup_config import ConfigImgRef as ecir
from setup_test.setup_config import ConfigROI as ecroi
from setup_test.setup_config import ConfigTouch as ect

image_directory = r"\\10.10.20.30\screenshot"

class SetupProcess:

    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    ocr_func = OCRManager()
    evaluation = Evaluation()
    modbus_label = ModbusLabels()
    search_pattern = os.path.join(image_directory, './**/*10.10.26.159*.png')
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
        self.static_text_measurement(
            image_path, "measurement", "mea_voltage", self.evaluation.label_voltage)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_2")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path1 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(
            image_path1, "measurement", "mea_current", self.evaluation.label_current)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_3")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path2 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(
            image_path2, "measurement", "mea_demand", self.evaluation.label_demand)
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_4")
        time.sleep(0.6)
        self.touch_manager.screenshot()
        time.sleep(0.6)
        image_path3 = self.load_image_file()
        time.sleep(1)
        self.static_text_measurement(
            image_path3, "measurement", "mea_power", self.evaluation.label_power)

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

        closest_file = min(self.file_time_diff,
                           key=self.file_time_diff.get, default=None)
        normalized_path = os.path.normpath(closest_file)
        self.latest_image_path = normalized_path

        print("가장 가까운 시간에 생성된 파일:", normalized_path)

        return self.latest_image_path

    def read_setup_mapping(self):
        modbus_results = self.modbus_label.read_all_modbus_values()
        for description, value in modbus_results.items():
            print(f"{description}: {value}")

    def static_text_measurement(self, image_path, color1, color2, select_ocr, roi_keys):
        test_image_path = image_path
        image = cv2.imread(test_image_path)
        color_result = self.ocr_func.color_detection(
            image, *self.coords_color[color1])
        color_result1 = self.ocr_func.color_detection(
            image, *self.coords_color[color2])

        if color_result < 5 and color_result1 < 5:
            roi_keys = ["1", "2", "5", "6", "9", "10", "13", "14"]
            cutted_image = self.ocr_func.ocr_basic(
                image=test_image_path, roi_keys=roi_keys)
            select_ocr = ["1"]
            ocr_error, right_error = self.evaluation.eval_static_text(
                cutted_image, select_ocr)
            if not ocr_error and not right_error:
                print("PASS")
            else:
                print("FAIL: different text")
        else:
            print("FAIL: different menu")

    def static_popup_text(self, image_path, select_ocr, roi_keys):
        test_image_path = image_path
        cutted_image = self.ocr_func.ocr_basic(
            image=test_image_path, roi_keys=roi_keys)
        ocr_error, right_error = self.evaluation.eval_static_text(
            cutted_image, select_ocr)
        if not ocr_error and not right_error:
            print("PASS")
        else:
            print("FAIL: different text")
        return

    def variable_text(self, image_path, select_ocr, roi_keys, roi_key):
        test_image_path = image_path

        # 첫 번째 이미지 처리
        cutted_images = self.ocr_func.ocr_basic(
            image=test_image_path, roi_keys=roi_keys)

        # 두 번째 이미지 처리
        ocr_calcul_results = self.ocr_func.ocr_basic(
            image=test_image_path, roi_keys=roi_key)

        # OCR 결과 비교
        ocr_error, right_error = self.evaluation.eval_demo_test(
            cutted_images, select_ocr, ocr_calcul_results)

        if not ocr_error and not right_error:
            print("PASS")
        else:
            print("FAIL: different text")

    def ocr_process(self, image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys=None, reset_time=None):
        """
        Args:
            image_path (str): The path to the image file.
            roi_keys (list): List of ROI keys for general OCR processing.
            roi_keys_meas (list): List of ROI keys for measurement OCR processing.
            ocr_ref (str): The OCR type to be selected for evaluation.
            time_keys (list): Min, Max time
            reset_time (time): Min, Max reset time
            img_result (str): image match curculation result
        Returns:
            None
        """
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
        
        if time_keys is not None:
            ocr_img_time = self.ocr_func.ocr_basic(image=image_path, roi_keys=time_keys)
            time_results = self.evaluation.check_time_diff(ocr_img_time, reset_time)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, ocr_img_time, time_results=time_results, img_path=image_path)
        else:
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path)

        return ocr_res

    def ocr_4phase(self, ref):  # A,B,C,Aver ###
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

    def ocr_curr_4phase(self, ref):  # A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                         "cur_percent_4", "a_meas", "b_meas", "c_meas", "aver_meas"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)

    def ocr_4phase_time(self, ref, reset_time):  # A,B,C,Aver + time stamp ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["a_meas", "b_meas", "c_meas", "aver_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp",
                     "c_time_stamp", "aver_time_stamp"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys,
                         roi_keys_meas, ocr_ref, time_keys, reset_time)

    def ocr_curr_4phase_time(self, ref, reset_time):  # A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca", "aver"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                         "cur_percent_4", "a_meas", "b_meas", "c_meas", "aver_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp",
                     "c_time_stamp", "aver_time_stamp"]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys,
                         roi_keys_meas, ocr_ref, time_keys, reset_time)

    def ocr_3phase(self, ref):  # A,B,C ###
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

    def ocr_3phase_time(self, ref, reset_time):  # A,B,C + time stamp ###
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
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time)

    def ocr_phaosr_process(self, img_ref, ref, img_cut1, img_cut2, img_cut3):
        self.touch_manager.screenshot()
        image_path = self.load_image_file()
        roi_keys = ["phasor_title", "phasor_vl_vn", "phasor_voltage",
                    "phasor_a_c_vol", "phasor_current", "phasor_a_c_cur"]
        roi_keys_meas = ["phasor_a_meas", "phasor_b_meas", "phasor_c_meas", "phasor_a_meas_cur", "phasor_b_meas_cur", "phasor_c_meas_cur",
                        "phasor_a_angle", "phasor_b_angle", "phasor_c_angle", "phasor_a_angle_cur", "phasor_b_angle_cur", "phasor_c_angle_cur"]
        ocr_ref = ref
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = []
        image_results.append(self.evaluation.img_match(image_path, img_cut1, img_ref))
        image_results.append(self.evaluation.img_match(image_path, img_cut2, img_ref))
        image_results.append(self.evaluation.img_match(image_path, img_cut3, img_ref))
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path, image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, img_result=image_results)

    def ocr_graph_detection(self, roi_keys, ocr_ref, value):
        self.touch_manager.screenshot()
        image_path = self.load_image_file()
        roi_keys = roi_keys
        ocr_ref = ocr_ref
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_detection(image_path, value, 2)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

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

    def __init__(self, stop_callback):
        self.stop_callback = stop_callback

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
        cutted_image = self.ocr_func.ocr_basic(
            image=image_path, roi_keys=roi_keys)
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
        cutted_image = self.ocr_func.ocr_basic(
            image=image_path, roi_keys=roi_keys)
        if "Password" in cutted_image:
            for _ in range(4):
                self.touch_manager.menu_touch("btn_num_pw_0")
            self.touch_manager.menu_touch("btn_num_pw_enter")
            self.touch_manager.menu_touch("cauiton_confirm")
            self.touch_manager.menu_touch("btn_apply")
        else:
            print("error")
            self.touch_manager.menu_touch("btn_popup_cencel")
        self.reset_time = datetime.now()
        print(self.reset_time)
        return self.reset_time

    def demo_mea_vol_rms(self):
        reset_time = self.modbus_label.reset_max_min()

        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.menu_touch("meas_L-L")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("rms_vol_L_L")
        if self.stop_callback():
            print("Test stopped")
            return

        ### L-L min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_L", reset_time)
        if self.stop_callback():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_L", reset_time)
        if self.stop_callback():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("rms_vol_L_N")
        if self.stop_callback():
            print("Test stopped")
            return

        ### L-N min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N", reset_time)
        if self.stop_callback():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N", reset_time)

        print("Voltage_RMS_Done")

    async def demo_mea_vol_fund(self):
        reset_time = self.modbus_label.reset_max_min()

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
        self.sp.ocr_4phase_time("fund_vol_L_L", reset_time)

        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_L", reset_time)

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("fund_vol_L_N")

        ### L-N min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_N", reset_time)

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_N", reset_time)

        print("Voltage_Fund_Done")

    def demo_mea_vol_thd(self):
        reset_time = self.modbus_label.reset_max_min()
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.menu_touch("thd_L_L")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("thd_vol_L_L")

        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("thd_vol_L_L", reset_time)

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("thd_L_N")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("thd_vol_L_N")

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("thd_vol_L_N", reset_time)

    def demo_mea_vol_freq(self):
        reset_time = self.modbus_label.reset_max_min()

        ### 기본주파수 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = "freq"
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)

        ### 주파수 Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = "freq"
        time_keys = ["a_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time)

        ### 주파수 Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = "freq"
        time_keys = ["a_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time)

    def demo_mea_vol_residual(self):
        reset_time = self.modbus_label.reset_max_min()

        ### 기본 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_5")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "vol_residual"
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)

        ### 잔류전압 Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "vol_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time)

        ### 잔류전압 Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "vol_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time)

    def demo_mea_curr_rms(self):
        reset_time = self.modbus_label.reset_max_min()

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
        self.sp.ocr_curr_4phase_time("rms_curr", reset_time)

        ### Current Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr", reset_time)

    def demo_mea_curr_fund(self):
        reset_time = self.modbus_label.reset_max_min()

        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("fund_curr")

        ### Current Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("fund_curr", reset_time)

        ### Current Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("fund_curr", reset_time)

    def demo_mea_curr_thd(self):
        reset_time = self.modbus_label.reset_max_min()

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
        self.sp.ocr_3phase_time("curr_thd", reset_time)

    def demo_mea_curr_tdd(self):
        reset_time = self.modbus_label.reset_max_min()

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
        self.sp.ocr_3phase_time("curr_tdd", reset_time)

    def demo_mea_curr_cf(self):
        reset_time = self.modbus_label.reset_max_min()

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
        self.sp.ocr_3phase_time("curr_cf", reset_time)

    def demo_mea_curr_kf(self):
        reset_time = self.modbus_label.reset_max_min()

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
        self.sp.ocr_3phase_time("curr_kf", reset_time)

    def demo_mea_curr_residual(self):
        reset_time = self.modbus_label.reset_max_min()

        ### Current residual ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_8")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "curr_residual"
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)

        ### Current residual Min###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "curr_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time)

        ### Current residual Max###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "curr_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time)

    def demo_mea_pow_active(self):
        reset_time = self.modbus_label.reset_max_min()

        ### active power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("active")
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("active", reset_time)
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("active", reset_time)
        
    def demo_mea_pow_reactive(self):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("reactive")
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("reactive", reset_time)
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("reactive", reset_time)
    
    def demo_mea_pow_apparent(self):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("apparent")
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("apparent", reset_time)
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("apparent", reset_time)
        
    def demo_mea_pow_pf(self):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("pf")
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("pf", reset_time)
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("pf", reset_time)
    
    def demo_mea_anal_phasor(self):
        ### voltage+current vll ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_1")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_all_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")

        ## voltage+current vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_all_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")

        ### voltage vll ###
        self.touch_manager.menu_touch("phas_har_curr")
        self.touch_manager.menu_touch("phasor_vll")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_vol_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")
        
        ### voltage vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_vol_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")

        ### current vll ###
        self.touch_manager.menu_touch("phas_har_curr")
        self.touch_manager.menu_touch("phas_har_vol")
        self.touch_manager.menu_touch("phasor_vll")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_curr_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")
        
        ### current vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_curr_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")
 
        ### nothing vll ###
        self.touch_manager.menu_touch("phas_har_curr")
        self.touch_manager.menu_touch("phasor_vll")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_na_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")
        
        ### nothing vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_na_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur")
 
    def demo_mea_anal_harmonics(self):
        ### voltage ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["harmonics_title", ecroi.harmonics_sub_title_1, "harmonics_sub_title_2",
                    "harmonics_text_A", "harmonics_text_B", "harmonics_text_C"]
        roi_keys_meas = ["harmonics_THD_A", "harmonics_THD_B", "harmonics_THD_C",
                         "harmonics_Fund_A", "harmonics_Fund_B", "harmonics_Fund_C"]
        ocr_ref = ec.harmonics_vol_3p4w
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, ecir.img_ref_harmonics_vol_3p4w.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

        ### current ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["harmonics_title", ecroi.harmonics_sub_title_1, "harmonics_sub_title_2",
                    "harmonics_text_A", "harmonics_text_B", "harmonics_text_C"]
        roi_keys_meas = ["harmonics_THD_A", "harmonics_THD_B", "harmonics_THD_C",
                         "harmonics_Fund_A", "harmonics_Fund_B", "harmonics_Fund_C"]
        ocr_ref = ec.harmonics_curr
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, ecir.img_ref_harmonics_curr.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

        ### vol_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_analysis_vol)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_a.value)

        ### vol_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_b.value)

        ### vol_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_c.value)

        ### curr_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_a.value)

        ### curr_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_b.value)

        ### curr_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_c.value)

        ### fund 버튼 후 vol_a ~ curr_c 반복 ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.touch_manager.menu_touch(ect.touch_analysis_vol)
        self.touch_manager.menu_touch(ect.touch_harmonics_fund)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_c.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_c.value)

        ### [v], fund, rms 그래프 변화 확인 ###
        ### voltage fund ###
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_fund)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_fund
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_vol_fund.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

        ### voltage rms ###
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_rms)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_rms
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_vol_rms.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

        ### current fund ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_fund)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_fund
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_curr_fund.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

        ### current rms ###
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_rms)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_rms
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_curr_rms.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

    def demo_mea_anal_waveform(self):

        ### waveform basic ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title]
        ocr_ref = ec.waveform_3p4w
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.waveform_all_img_cut, ecir.img_ref_waveform_all.value,)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results)

        ### waveform vol_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_a)
        self.sp.ocr_graph_detection(ecroi.color_waveform_vol_a.value)

        ### waveform vol_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_a)
        self.touch_manager.menu_touch(ect.touch_wave_vol_b)
        self.sp.ocr_graph_detection(ecroi.color_waveform_vol_b.value)

        ### waveform vol_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_b)
        self.touch_manager.menu_touch(ect.touch_wave_vol_c)
        self.sp.ocr_graph_detection(ecroi.color_waveform_vol_c.value)

        ### waveform curr_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_c)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection(ecroi.color_waveform_curr_a.value)

        ### waveform curr_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection(ecroi.color_waveform_curr_b.value)

        ### waveform curr_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection(ecroi.color_waveform_curr_c.value)
     
    def demo_mea_anal_voltsym(self):
        ### LL ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "a_meas", "b_meas"]
        ocr_ref = "volt_sym"
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
        
        ### LL Max###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "a_meas", "b_meas"]
        ocr_ref = "volt_sym"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
        ### LN ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("thd_L_N")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "a_meas", "b_meas"]
        ocr_ref = "volt_sym"
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref)
        
        ### LN Max###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "a_meas", "b_meas"]
        ocr_ref = "volt_sym"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys)
        
    def demo_mea_anal_voltunbal(self):
        ### vol unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_5")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.unbal_vol)
        
        ### vol unbalance max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.unbal_vol)
        
    def demo_mea_anal_cursym(self):
        ### symm ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_6")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.symm_curr)
        
        ### symm max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.symm_curr)
        
    def demo_mea_anal_currunbal(self):
        ### symm ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_7")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.symm_curr)
        
        ### symm max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.symm_curr)

    def testcode01(self):
        image_path = r"C:\Users\Jin\Desktop\Company\Rootech\PNT\AutoProgram\csvtest\2024-08-29_10_35_06_M_H_AN_Harmonics.png"
        roi_keys = [ecroi.harmonics_text_title ,ecroi.harmonics_text_img]
        roi_keys_meas = ["harmonics_THD_A", "harmonics_THD_B", "harmonics_THD_C",
                         "harmonics_Fund_A", "harmonics_Fund_B", "harmonics_Fund_C"]
        ocr_ref = ec.harmonics_vol_3p4w
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        result = re.sub(r'[0-9.\s]', '', ocr_img[1])
        if not result.strip() == None:
            print("None")
        else:
            print(result)

        print("Done")

    def demo_test_start(self):
        # self.modbus_label.demo_test_setting()
        print("----------------DEMO TEST START----------------")
        
    def demo_test_voltage(self):
        self.demo_mea_vol_rms()
        self.demo_mea_vol_fund()
        self.demo_mea_vol_thd()
        self.demo_mea_vol_freq()
        self.demo_mea_vol_residual()
        print("Done")
        
    def demo_test_current(self):
        self.demo_mea_curr_rms()
        self.demo_mea_curr_fund()
        self.demo_mea_curr_thd()
        self.demo_mea_curr_tdd()
        self.demo_mea_curr_cf()
        self.demo_mea_curr_kf()
        self.demo_mea_curr_residual()
        print("Done")
        
    def demo_test_power(self):
        self.demo_mea_pow_active()
        self.demo_mea_pow_reactive()
        self.demo_mea_pow_apparent()
        self.demo_mea_pow_pf()
        print("Done")
        
    def demo_test_analysis(self):
        # self.demo_mea_anal_phasor()
        self.demo_mea_anal_harmonics()
        # self.demo_mea_anal_waveform()
        print("Done")

    def testcode03(self):
        # self.modbus_label.demo_test_setting()
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["phasor_title", "phasor_vl_vn", "phasor_voltage",
                    "phasor_a_c_vol", "phasor_current", "phasor_a_c_cur"]
        roi_keys_meas = ["phasor_a_meas", "phasor_b_meas", "phasor_c_meas", "phasor_a_meas_cur", "phasor_b_meas_cur", "phasor_c_meas_cur",
                         "phasor_a_angle", "phasor_b_angle", "phasor_c_angle", "phasor_a_angle_cur", "phasor_b_angle_cur", "phasor_c_angle_cur"]
        ocr_ref = "phasor_L_L"
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_result = self.evaluation.img_match(image_path, "phasor_img_cut", ecir.img_ref_phasor_all_vll.value)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path, image_result)
    
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, img_result=image_result)
           