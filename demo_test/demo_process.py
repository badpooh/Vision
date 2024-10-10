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
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
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
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.curr_per_aver, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
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
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp,
                     ecroi.c_time_stamp, ecroi.aver_time_stamp]
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
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.curr_per_aver, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp,
                     ecroi.c_time_stamp, ecroi.aver_time_stamp]
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
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
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
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp, ecroi.c_time_stamp]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)

    def ocr_phaosr_process(self, img_ref, ref, img_cut1, img_cut2, img_cut3, base_save_path):
        self.touch_manager.screenshot()
        image_path = self.load_image_file()
        roi_keys = [ecroi.phasor_title, ecroi.phasor_vl_vn, ecroi.phasor_voltage, ecroi.phasor_a_c_vol, ecroi.phasor_current, ecroi.phasor_a_c_cur]
        roi_keys_meas = [ecroi.phasor_a_meas, ecroi.phasor_b_meas, ecroi.phasor_c_meas, ecroi.phasor_a_meas_cur, ecroi.phasor_b_meas_cur, ecroi.phasor_c_meas_cur,
                        ecroi.phasor_a_angle, ecroi.phasor_b_angle, ecroi.phasor_c_angle, ecroi.phasor_a_angle_cur, ecroi.phasor_b_angle_cur, ecroi.phasor_c_angle_cur]
        ocr_ref = ref
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = []
        image_results.append(self.evaluation.img_match(image_path, img_cut1, img_ref))
        image_results.append(self.evaluation.img_match(image_path, img_cut2, img_ref))
        image_results.append(self.evaluation.img_match(image_path, img_cut3, img_ref))
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path, image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, img_result=image_results, base_save_path=base_save_path)

    def ocr_graph_detection(self, roi_keys, ocr_ref, value, base_save_path):
        self.touch_manager.screenshot()
        image_path = self.load_image_file()
        roi_keys = roi_keys
        ocr_ref = ocr_ref
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_detection(image_path, value, 2)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
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
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_3.value)
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
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_1.value)
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
        self.touch_manager.menu_touch(ect.touch_main_menu_1.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_1.value)
        self.touch_manager.menu_touch(ect.touch_meas_ll.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(ec.rms_vol_ll.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L min 검사 ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.rms_vol_ll.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.rms_vol_ll.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.menu_touch(ect.touch_meas_ln.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(ec.rms_vol_ln.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N min 검사 ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.rms_vol_ln.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.rms_vol_ln.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        print("Voltage_RMS_Done")

    def demo_mea_vol_fund(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_1.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_meas_ll.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(ec.fund_vol_ll.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L min 검사 ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.fund_vol_ll.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.fund_vol_ll.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.menu_touch(ect.touch_meas_ln.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(ec.fund_vol_ln.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N min 검사 ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.fund_vol_ln.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(ec.fund_vol_ln.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        print("Voltage_Fund_Done")

    def demo_mea_vol_thd(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_1.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_3.value)
        self.touch_manager.menu_touch(ect.touch_thd_ll.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(ec.thd_vol_ll.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-L max 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(ec.thd_vol_ll.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N 만 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.menu_touch(ect.touch_thd_ln.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(ec.thd_vol_ln.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### L-N max 검사 ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(ec.thd_vol_ln.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_vol_freq(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### 기본주파수 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_1.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab]
        roi_keys_meas = [ecroi.a_meas]
        ocr_ref = ec.freq.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 주파수 Min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab]
        roi_keys_meas = [ecroi.a_meas]
        ocr_ref = ec.freq.value
        time_keys = [ecroi.a_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 주파수 Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab]
        roi_keys_meas = [ecroi.a_meas]
        ocr_ref = ec.freq.value
        time_keys = [ecroi.a_time_stamp]
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
        self.touch_manager.menu_touch(ect.touch_main_menu_1.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_5.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.residual_vol.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 잔류전압 Min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.residual_vol.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### 잔류전압 Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.residual_vol.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
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
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_1.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.rms_curr.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.rms_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.rms_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_fund(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_2.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.fund_curr.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.fund_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.fund_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_thd(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current thd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(ec.thd_curr.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current thd Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(ec.thd_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_tdd(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current tdd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_5.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(ec.tdd_curr.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current tdd Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(ec.tdd_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_cf(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current crest factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_6.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(ec.cf_curr.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current crest factor Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(ec.cf_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_kf(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current k-factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_7.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(ec.kf_curr.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current k-factor Max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(ec.kf_curr.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_curr_residual(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### Current residual ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_8.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.residual_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current residual Min###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.residual_curr.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### Current residual Max###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.residual_curr.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
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
        self.touch_manager.menu_touch(ect.touch_main_menu_3.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_1.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.active.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.active.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.active.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_mea_pow_reactive(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_3.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_2.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.reactive.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.reactive.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.reactive.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
    
    def demo_mea_pow_apparent(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_3.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_3.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.apparent.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.apparent.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.apparent.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_mea_pow_pf(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()

        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_3.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.pf.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power min ###
        self.touch_manager.menu_touch(ect.touch_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.pf.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
        ### power max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.pf.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
    
    def demo_mea_anal_phasor(self, base_save_path):
        ### voltage+current vll ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_1.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_all_vll.value, ref=ec.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        

        ## voltage+current vln ###
        self.touch_manager.menu_touch(ect.touch_phasor_vln.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_all_vln.value, ref=ec.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### voltage vll ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.menu_touch(ect.touch_phasor_vll.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_vol_vll.value, ref=ec.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### voltage vln ###
        self.touch_manager.menu_touch(ect.touch_phasor_vln.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_vol_vln.value, ref=ec.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current vll ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.menu_touch(ect.touch_analysis_vol.value)
        self.touch_manager.menu_touch(ect.touch_phasor_vll.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_curr_vll.value, ref=ec.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current vln ###
        self.touch_manager.menu_touch(ect.touch_phasor_vln.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_curr_vln.value, ref=ec.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### nothing vll ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.menu_touch(ect.touch_phasor_vll.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_na_vll.value, ref=ec.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### nothing vln ###
        self.touch_manager.menu_touch(ect.touch_phasor_vln.value)
        self.sp.ocr_phaosr_process(img_ref=ecir.img_ref_phasor_na_vln.value, ref=ec.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_harmonics(self, base_save_path):
        ### voltage ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_2.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.harmonics_title, ecroi.harmonics_sub_title_1, ecroi.harmonics_sub_title_2,
                    ecroi.harmonics_graph_a, ecroi.harmonics_graph_b, ecroi.harmonics_graph_c]
        roi_keys_meas = [ecroi.harmonics_thd_a, ecroi.harmonics_thd_b, ecroi.harmonics_thd_c,
                         ecroi.harmonics_fund_a, ecroi.harmonics_fund_b, ecroi.harmonics_fund_c]
        ocr_ref = ec.harmonics_vol_3p4w.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, ecir.img_ref_harmonics_vol_3p4w.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.harmonics_title, ecroi.harmonics_sub_title_1, ecroi.harmonics_sub_title_2,
                    ecroi.harmonics_graph_a, ecroi.harmonics_graph_b, ecroi.harmonics_graph_c]
        roi_keys_meas = [ecroi.harmonics_thd_a, ecroi.harmonics_thd_b, ecroi.harmonics_thd_c,
                         ecroi.harmonics_fund_a, ecroi.harmonics_fund_b, ecroi.harmonics_fund_c]
        ocr_ref = ec.harmonics_curr.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, ecir.img_ref_harmonics_curr.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_analysis_vol.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_vol_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_vol_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### curr_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_curr_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### curr_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_curr_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### curr_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_curr_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### fund 버튼 후 vol_a ~ curr_c 반복 ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.touch_manager.menu_touch(ect.touch_analysis_vol.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_fund.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_vol_b.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_vol_c.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_curr_a.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_curr_b.value, base_save_path=base_save_path)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.harmonics_for_img.value, value=ecroi.color_harmonics_curr_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### [v], fund, rms 그래프 변화 확인 ###
        ### voltage fund ###
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_fund.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_fund.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_vol_fund.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### voltage rms ###
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_rms.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_rms.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_vol_rms.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current fund ###
        self.touch_manager.menu_touch(ect.touch_analysis_curr.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_fund.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_fund.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_curr_fund.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### current rms ###
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_1.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_rms.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title, ecroi.harmonics_sub_title_1]
        ocr_ref = ec.harmonics_per_rms.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, ecir.img_ref_harmonics_curr_rms.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_meter_harmonics_text(self, base_save_path):
        ### voltage ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_submenu_2.value)
        self.touch_manager.menu_touch(ect.touch_harmonics_sub_text.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_key = [ecroi.harmonics_title, ecroi.harmonics_text_sub_title, ecroi.harmonics_text_sub_abc]
        roi_keys = [ecroi.harmonics_text_chart_img_cut]
        ocr_ref = ec.harmonics_text.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_key)
        validate_ocr_results = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        invalid_elements = self.evaluation.validate_ocr(validate_ocr_results)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path)
        self.evaluation.save_csv(ocr_img=ocr_img, ocr_error=ocr_error, right_error=right_error, meas_error=meas_error, img_path=image_path,base_save_path=base_save_path, invalid_elements=invalid_elements)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_mea_anal_waveform(self, base_save_path):
        ### waveform basic ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_3.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.waveform_title]
        ocr_ref = ec.waveform_3p4w.value
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.waveform_all_img_cut, ecir.img_ref_waveform_all.value,)
        ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform vol_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_a.value)
        self.sp.ocr_graph_detection(roi_keys=[ecroi.waveform_title], ocr_ref=ec.waveform_3p4w.value, value=ecroi.color_waveform_vol_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform vol_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_vol_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w.value, ecroi.color_waveform_vol_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform vol_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_vol_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w.value, ecroi.color_waveform_vol_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform curr_a-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_vol_c.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w.value, ecroi.color_waveform_curr_a.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform curr_b-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_a.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w.value, ecroi.color_waveform_curr_b.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### waveform curr_c-phase X ###
        self.touch_manager.menu_touch(ect.touch_wave_curr_b.value)
        self.touch_manager.menu_touch(ect.touch_wave_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], ec.waveform_3p4w.value, ecroi.color_waveform_curr_c.value, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_voltsym(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### LL ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.symm_vol_ll.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### LL Max###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.a_meas, ecroi.b_meas]
        ocr_ref = ec.symm_vol_ll.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### LN ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.menu_touch(ect.touch_thd_ln.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = ec.symm_vol_ln.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### LN Max###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = ec.symm_vol_ln.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_voltunbal(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### vol unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_5.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(ec.unbal_vol.value, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### vol unbalance max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(ec.unbal_vol.value, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_cursym(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### symm ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_6.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = ec.symm_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### symm max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp, ecroi.c_time_stamp]
        ocr_ref = ec.symm_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

    def demo_mea_anal_currunbal(self, base_save_path):
        reset_time = self.modbus_label.reset_max_min()
        ### current unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_7.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = ec.unbal_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return

        ### symm max ###
        self.touch_manager.menu_touch(ect.touch_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp, ecroi.c_time_stamp]
        ocr_ref = ec.unbal_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        
    def demo_meter_demand_curr(self, base_save_path):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_2.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_3.value)
        self.sp.ocr_curr_4phase(ec.demand_current.value, base_save_path)
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
        self.demo_meter_demand_curr(base_save_path)
        if self.stop_event.is_set():
            print("Test stopped")
            return
        

    def testcode01(self):
            image_path = r"C:\Users\Jin\Desktop\test_11.png"
            reset_time = datetime.now()
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            base_save_path = os.path.expanduser(f"./results/{current_time}/")
            os.makedirs(base_save_path, exist_ok=True)
            roi_key = [ecroi.harmonics_title, ecroi.harmonics_text_sub_title, ecroi.harmonics_text_sub_abc]
            roi_keys = [ecroi.harmonics_text_chart_img_cut]
            ocr_ref = ec.harmonics_text.value
            ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_key)
            validate_ocr_results = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
            invalid_elements = self.evaluation.validate_ocr(validate_ocr_results)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path)
            self.evaluation.save_csv(ocr_img=ocr_img, ocr_error=ocr_error, right_error=right_error, meas_error=meas_error, img_path=image_path,base_save_path=base_save_path, invalid_elements=invalid_elements)
            if self.stop_event.is_set():
                print("Test stopped")
                return
                  
    def testcode03(self):
        # self.modbus_label.demo_test_setting()
        # self.touch_manager.btn_front_meter()
        # self.touch_manager.btn_front_home()
        self.touch_manager.menu_touch(ect.touch_main_menu_4.value)
        self.touch_manager.menu_touch(ect.touch_side_menu_1.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["phasor_title", "phasor_vl_vn", "phasor_voltage",
                    "phasor_a_c_vol", "phasor_current", "phasor_a_c_cur"]
        roi_keys_meas = ["phasor_a_meas", "phasor_b_meas", "phasor_c_meas", "phasor_a_meas_cur", "phasor_b_meas_cur", "phasor_c_meas_cur",
                         "phasor_a_angle", "phasor_b_angle", "phasor_c_angle", "phasor_a_angle_cur", "phasor_b_angle_cur", "phasor_c_angle_cur"]
        ocr_ref = ec.phasor_ll
        ocr_img = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = self.ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_result = self.evaluation.img_match(image_path, "phasor_img_cut", ecir.img_ref_phasor_all_vll.value)
        ocr_error, right_error, meas_error, ocr_res = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path, image_result)
    
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, img_result=image_result)
           