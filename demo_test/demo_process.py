import cv2
import numpy as np
import os
import glob
from datetime import datetime
import time
import re

from demo_test.demo_function import TouchManager, ModbusManager, OCRManager, Evaluation, ModbusLabels
from demo_test.demo_config import ConfigTextRef as ec
from demo_test.demo_config import ConfigImgRef as ecir
from demo_test.demo_config import ConfigROI as ecroi
from demo_test.demo_config import ConfigTouch as ect

image_directory = r"\\10.10.20.30\screenshot"


class DemoProcess:

    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    ocr_func = OCRManager()
    evaluation = Evaluation()
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

    def ocr_process(self, image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys=None, reset_time=None, base_save_path=None):
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
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
        
        if time_keys is not None:
            ocr_img_time = self.ocr_func.ocr_basic(image=image_path, roi_keys=time_keys)
            time_results = self.evaluation.check_time_diff(ocr_img_time, reset_time)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, ocr_img_time, time_results=time_results, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)
        else:
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)

        return ocr_res

    def ocr_4phase(self, ref, base_save_path):  # A,B,C,Aver ###
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
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)

    def ocr_curr_4phase(self, ref, base_save_path):  # A,B,C,Aver ###
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
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)

    def ocr_4phase_time(self, ref, reset_time, base_save_path):  # A,B,C,Aver + time stamp ###
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
                         roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)

    def ocr_curr_4phase_time(self, ref, reset_time, base_save_path):  # A,B,C,Aver ###
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
                         roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)

    def ocr_3phase(self, ref, base_save_path):  # A,B,C ###
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
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)

    def ocr_3phase_time(self, ref, reset_time, base_save_path):  # A,B,C + time stamp ###
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
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)

    def ocr_phaosr_process(self, img_ref, ref, img_cut1, img_cut2, img_cut3, base_save_path):
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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, img_result=image_results, base_save_path=base_save_path)

    def ocr_graph_detection(self, roi_keys, ocr_ref, value, base_save_path):
        self.touch_manager.screenshot()
        image_path = self.load_image_file()
        roi_keys = roi_keys
        ocr_ref = ocr_ref
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_detection(image_path, value, 2)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)

class DemoTest:

    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    modbus_label = ModbusLabels()
    ocr_func = OCRManager()
    evaluation = Evaluation()
    sp = DemoProcess()
    search_pattern = os.path.join(image_directory, './**/*10.10.26.156*.png')
    now = datetime.now()
    file_time_diff = {}

    def __init__(self, stop_event):
        self.stop_event = stop_event

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

    def demo_mea_vol_rms(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.menu_touch("meas_L-L")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("rms_vol_L_L", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_L", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_L", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("rms_vol_L_N", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("rms_vol_L_N", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        print("Voltage_RMS_Done")

    def demo_mea_vol_fund(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.menu_touch("meas_L-L")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("fund_vol_L_L", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_L", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_L", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("meas_L-N")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase("fund_vol_L_N", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N min 검사 ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_N", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time("fund_vol_L_N", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        print("Voltage_Fund_Done")

    def demo_mea_vol_thd(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_1")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.menu_touch("thd_L_L")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("thd_vol_L_L", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("thd_vol_L_L", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("thd_L_N")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("thd_vol_L_N", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("thd_vol_L_N", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_vol_freq(self, base_save_path):
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
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 주파수 Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = "freq"
        time_keys = ["a_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 주파수 Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab"]
        roi_keys_meas = ["a_meas"]
        ocr_ref = "freq"
        time_keys = ["a_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_vol_residual(self, base_save_path):
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
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 잔류전압 Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "vol_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 잔류전압 Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "vol_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_rms(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("rms_curr", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("rms_curr", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_fund(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("fund_curr", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("fund_curr", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("fund_curr", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_thd(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current thd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_thd", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current thd Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_thd", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_tdd(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current tdd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_5")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_tdd", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current tdd Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_tdd", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_cf(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current crest factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_6")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_cf", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current crest factor Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_cf", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_kf(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current k-factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_2")
        self.touch_manager.menu_touch("side_menu_7")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase("curr_kf", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current k-factor Max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time("curr_kf", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_residual(self, base_save_path):
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
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current residual Min###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "curr_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current residual Max###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["a_meas", "b_meas"]
        ocr_ref = "curr_residual"
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_pow_active(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### active power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_1")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("active", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("active", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("active", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_mea_pow_reactive(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_2")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("reactive", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("reactive", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("reactive", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
    
    def demo_mea_pow_apparent(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_3")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("apparent", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("apparent", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("apparent", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_mea_pow_pf(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_3")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase("pf", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch("Min")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("pf", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time("pf", reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
    
    def demo_mea_anal_phasor(self, base_save_path):
        ### voltage+current vll ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_1")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_all_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ## voltage+current vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_all_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### voltage vll ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch("phasor_vll")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_vol_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### voltage vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_vol_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current vll ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch(ect.touch_analysis_vol)
        self.touch_manager.menu_touch("phasor_vll")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_curr_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_curr_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### nothing vll ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch("phasor_vll")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_na_vll.value, "phasor_L_L", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### nothing vln ###
        self.touch_manager.menu_touch("phasor_vln")
        self.sp.ocr_phaosr_process(ecir.img_ref_phasor_na_vln.value, "phasor_L_N", "phasor_img_cut", "phasor_a_c_angle_vol", "phasor_a_c_angle_cur", base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_harmonics(self, base_save_path):
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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_analysis_vol)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### curr_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### curr_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### curr_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### fund 버튼 후 vol_a ~ curr_c 반복 ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.touch_manager.menu_touch(ect.touch_analysis_vol)
        self.touch_manager.menu_touch(ect.touch_harmonics_fund)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_b.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_vol_c.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.touch_manager.menu_touch(ect.touch_analysis_curr)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_a.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_b.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img, value=ecroi.color_harmonics_curr_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_waveform(self, base_save_path):
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
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform vol_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_a)
        self.sp.ocr_graph_detection(roi_keys=[ecroi.waveform_title], ocr_ref=ec.waveform_3p4w, value=ecroi.color_waveform_vol_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform vol_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_a)
        self.touch_manager.menu_touch(ect.touch_wave_vol_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w, ecroi.color_waveform_vol_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform vol_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_b)
        self.touch_manager.menu_touch(ect.touch_wave_vol_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w, ecroi.color_waveform_vol_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform curr_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_c)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w, ecroi.color_waveform_curr_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform curr_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w, ecroi.color_waveform_curr_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform curr_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w, ecroi.color_waveform_curr_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_voltsym(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### LL ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_4")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "a_meas", "b_meas"]
        ocr_ref = ec.symm_vol_ll
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### LL Max###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "a_meas", "b_meas"]
        ocr_ref = ec.symm_vol_ll
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### LN ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.menu_touch("thd_L_N")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3", "a_meas", "b_meas", "c_meas"]
        ocr_ref = ec.symm_vol_ln
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### LN Max###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3", "a_meas", "b_meas", "c_meas"]
        ocr_ref = ec.symm_vol_ln
        time_keys = ["a_time_stamp", "b_time_stamp"]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_voltunbal(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### vol unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_5")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.unbal_vol, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol unbalance max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.unbal_vol, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_cursym(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### symm ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_6")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                         "a_meas", "b_meas", "c_meas"]
        ocr_ref = ec.symm_curr
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### symm max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                         "a_meas", "b_meas", "c_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp", "c_time_stamp"]
        ocr_ref = ec.symm_curr
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_currunbal(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### current unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch("main_menu_4")
        self.touch_manager.menu_touch("side_menu_7")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                         "a_meas", "b_meas", "c_meas"]
        ocr_ref = ec.unbal_curr
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### symm max ###
        self.touch_manager.menu_touch("Max")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
        roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                         "a_meas", "b_meas", "c_meas"]
        time_keys = ["a_time_stamp", "b_time_stamp", "c_time_stamp"]
        ocr_ref = ec.unbal_curr
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_meter_demand_curr(self, base_save_path):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch()
        pass

    def demo_test_start(self):
        self.modbus_label.demo_test_setting()
        print("----------------DEMO TEST START----------------")
        
    def demo_test_voltage(self, base_save_path):
        self.demo_mea_vol_rms(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_vol_fund(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_vol_thd(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_vol_freq(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_vol_residual(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_test_current(self, base_save_path):
        self.demo_mea_curr_rms(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_curr_fund(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_curr_thd(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_curr_tdd(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_curr_cf(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_curr_kf(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_curr_residual(base_save_path)
        
    def demo_test_power(self, base_save_path):
        self.demo_mea_pow_active(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_pow_reactive(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_pow_apparent(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_pow_pf(base_save_path)
        
    def demo_test_analysis(self, base_save_path):
        self.demo_mea_anal_phasor(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_anal_harmonics(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_anal_waveform(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_anal_voltsym(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_anal_voltunbal(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_anal_cursym(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        self.demo_mea_anal_currunbal(base_save_path)

    def demo_test_demand(self, base_save_path):
        pass
        

    def testcode01(self):
            image_path = r"C:\Users\Jin\Desktop\Company\Rootech\PNT\AutoProgram\image_test\10.10.26.159_2024-08-13_17_28_37_M_H_AN_Curr_Unbal.png"
            reset_time = datetime.now()
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            base_save_path = os.path.expanduser(f"./results/{current_time}/")
            os.makedirs(base_save_path, exist_ok=True)
            roi_keys = ["title_view", "a_ab", "b_bc", "c_ca"]
            roi_keys_meas = ["cur_percent_1", "cur_percent_2", "cur_percent_3",
                            "a_meas", "b_meas", "c_meas"]
            time_keys = ["a_time_stamp", "b_time_stamp", "c_time_stamp"]
            ocr_ref = ec.unbal_curr
            self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)

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
           