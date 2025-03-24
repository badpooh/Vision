import time
from function.func_ocr import PaddleOCRManager
from function.func_ocr import EasyOCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation
from function.func_autogui import AutoGUI

from config.config_touch import ConfigTouch as cft
from config.config_roi import ConfigROI as cfr
from config.config_map import ConfigModbusMap as ecm
from config.config_map import ConfigInitialValue as civ
from config.config_ref import ConfigImgRef

image_directory = r"\\10.10.20.30\screenshot"
paddleocr_func = PaddleOCRManager()
easyocr_func = EasyOCRManager()

class SetupTest:
     
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()
	eval_manager = Evaluation()
	autogui_manager = AutoGUI()

	def __init__(self):
		pass

	def setup_ocr_process(self, base_save_path, search_pattern, roi_keys, except_address, access_address, ref_value, template_path, coordinates=None):
		"""
		Args:
			base_save_path (str): 결과 저장 디렉토리
			search_pattern (str): 스크린샷 파일 검색 패턴
			roi_keys (list): ROI 키 (길이 2 이상 가정)
			except_address (Enum): 검사에서 제외할 단일 주소 (ex: ecm.addr_wiring)
			access_address (tuple): 측정 접근 주소 (ex: (6000,1))
			template_path: AccuraSM 정답 png 파일
			coordinates (list): 미정
		Returns:
			None
		"""
		self.touch_manager.screenshot()
		image_path = self.eval_manager.load_image_file(search_pattern)
		setup = 1
		ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys, test_type=setup)
		except_addr = {except_address}
		target_address = except_address
		reference_value = ref_value
		compare_title = roi_keys[0].value[0]
		ref_title_1 = roi_keys[1].value[0]
		ref_title_2 = roi_keys[1].value[1]
		self.autogui_manager.m_s_meas_refresh(image_path, base_save_path, compare_title)
		time.sleep(0.6)
		sm_res, sm_condition = self.autogui_manager.find_and_click(template_path, image_path, base_save_path, compare_title)
		title, setup_result, modbus_result, overall_result = self.eval_manager.eval_setup_test(
			ocr_res=ocr_results,
			setup_ref=reference_value,
			title=compare_title,
			ecm_access_address=access_address,
			ecm_address=target_address,
			setup_ref_title_1=ref_title_1,
			setup_ref_title_2=ref_title_2,
			except_addr=except_addr,
			sm_res=sm_res,
			sm_condition = sm_condition
			)
		self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result, title)
		time.sleep(0.5)
		
	def setup_meter_s_m_vol(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		### wiring -> Delta
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()
		self.touch_manager.touch_menu(cft.touch_main_menu_1.value)
		self.touch_manager.touch_menu(cft.touch_side_menu_1.value)
		self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		self.touch_manager.touch_password()
		self.touch_manager.touch_menu(cft.touch_btn_popup_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_wiring_1, cfr.s_wiring_2]
		except_addr = ecm.addr_wiring
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_wiring_delta
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		
		### wiring -> Wye
		self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_wiring_1, cfr.s_wiring_2]
		except_addr = ecm.addr_wiring
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_wiring_wye
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)

		## min.meas.secondary l-n volt 5-> 0
		self.touch_manager.touch_menu(cft.touch_data_view_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_0.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_min_meas_sec_ln_vol_1, cfr.s_min_meas_sec_ln_vol_2]
		except_addr = ecm.addr_min_measured_secondary_ln_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_min_meas_secondary_ln_vol_0
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		
		### min.meas.secondary l-n volt 0-> 11
		self.touch_manager.touch_menu(cft.touch_data_view_2.value)
		for i in range(2):
			self.touch_manager.touch_menu(cft.touch_btn_number_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_min_meas_sec_ln_vol_1, cfr.s_min_meas_sec_ln_vol_2]
		except_addr = ecm.addr_min_measured_secondary_ln_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_min_meas_secondary_ln_vol_10
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### min.meas.secondary l-n volt 초기화
		self.modbus_label.setup_target_initialize(ecm.addr_measurement_setup_access, ecm.addr_min_measured_secondary_ln_voltage, bit16=5)

		## VT Primary L-L Voltage 49 --> roi 2번 좌표가 아래로 뒤집어짐? 좌표 확인 필요
		self.touch_manager.touch_menu(cft.touch_data_view_3.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_4.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_9.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_vt_primary_ll_vol_1, cfr.s_vt_primary_ll_vol_2]
		except_addr = ecm.addr_vt_primary_ll_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_vt_primary_ll_vol_50
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)

		## VT Primary L-L Voltage 1000000
		self.touch_manager.touch_menu(cft.touch_data_view_3.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_1.value)
		for i in range(6):
			self.touch_manager.touch_menu(cft.touch_btn_number_0.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_vt_primary_ll_vol_1, cfr.s_vt_primary_ll_vol_2]
		except_addr = ecm.addr_vt_primary_ll_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_vt_primary_ll_vol_999999
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ecm.addr_measurement_setup_access, ecm.addr_vt_primary_ll_voltage, bit32=1900)

		### VT Secondary L-L Voltage 49
		self.touch_manager.touch_menu(cft.touch_data_view_4.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_4.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_9.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_vt_secondary_ll_vol_1, cfr.s_vt_secondary_ll_vol_2]
		except_addr = ecm.addr_vt_secondary_ll_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_vt_secondary_ll_vol_50
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### VT Secondary L-L Voltage 221
		self.touch_manager.touch_menu(cft.touch_data_view_4.value)
		for i in range(2):
			self.touch_manager.touch_menu(cft.touch_btn_number_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_vt_secondary_ll_vol_1, cfr.s_vt_secondary_ll_vol_2]
		except_addr = ecm.addr_vt_secondary_ll_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_vt_secondary_ll_vol_220
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ecm.addr_measurement_setup_access, ecm.addr_vt_secondary_ll_voltage, bit16=1900)

		### Primary Reference Voltage L-L -> L-N
		self.touch_manager.touch_menu(cft.touch_data_view_5.value)
		self.touch_manager.touch_menu(cft.touch_btn_ref_ln.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_primary_reference_vol_1, cfr.s_primary_reference_vol_2]
		except_addr = ecm.addr_reference_voltage_mode
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_primary_reference_vol_mode_ln
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### Primary Reference Voltage L-N -> L-L
		self.touch_manager.touch_menu(cft.touch_data_view_5.value)
		self.touch_manager.touch_menu(cft.touch_btn_ref_ll.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_primary_reference_vol_1, cfr.s_primary_reference_vol_2]
		except_addr = ecm.addr_reference_voltage_mode
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_primary_reference_vol_mode_ll
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)

		### Primary Reference Voltage 49
		self.touch_manager.touch_menu(cft.touch_data_view_5.value)
		self.touch_manager.touch_menu(cft.touch_btn_ref_num_4.value)
		self.touch_manager.touch_menu(cft.touch_btn_ref_num_9.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_primary_reference_vol_1, cfr.s_primary_reference_vol_3]
		except_addr = ecm.addr_reference_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_primary_reference_vol_50
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### Primary Reference Voltage 1000000
		self.touch_manager.touch_menu(cft.touch_data_view_5.value)
		self.touch_manager.touch_menu(cft.touch_btn_ref_num_1.value)
		for i in range(6):
			self.touch_manager.touch_menu(cft.touch_btn_ref_num_0.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_primary_reference_vol_1, cfr.s_primary_reference_vol_3]
		except_addr = ecm.addr_reference_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_primary_reference_vol_999999
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ecm.addr_measurement_setup_access, ecm.addr_reference_voltage, bit32=1900)

		### Sliding Reference Voltage Disable -> Enable
		self.touch_manager.touch_menu(cft.touch_data_view_6.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_sliding_reference_vol_1, cfr.s_sliding_reference_vol_2]
		except_addr = ecm.addr_sliding_reference_voltage_type
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_sliding_reference_vol_enable
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_sliding_reference_voltage_setup_access.value, ref_value=ref_value, template_path=template_path)
		### Sliding Reference Voltage Enable -> Disable
		self.touch_manager.touch_menu(cft.touch_data_view_6.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_sliding_reference_vol_1, cfr.s_sliding_reference_vol_2]
		except_addr = ecm.addr_sliding_reference_voltage_type
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_sliding_reference_vol_disable
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_sliding_reference_voltage_setup_access.value, ref_value=ref_value, template_path=template_path)

		### Rotating Sequence Positive -> Negative
		self.touch_manager.touch_menu(cft.touch_data_view_7.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_rotation_sequence_1, cfr.s_rotation_sequence_1]
		except_addr = ecm.addr_rotating_sequence
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_rotating_sequence_negative
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)
		### Rotating Sequence Negative -> Positive
		self.touch_manager.touch_menu(cft.touch_data_view_6.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_rotation_sequence_1, cfr.s_rotation_sequence_1]
		except_addr = ecm.addr_rotating_sequence
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_rotating_sequence_positive
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path)

	def setup_meter_s_m_curr(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		### CT Primary Current 50 -> 5 (4로 변경)
		# self.touch_manager.btn_front_meter()
		# self.touch_manager.btn_front_setup()
		# self.touch_manager.touch_menu(cft.touch_main_menu_1.value)
		# self.touch_manager.touch_menu(cft.touch_side_menu_2.value)
		# self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		# self.touch_manager.touch_password()
		# self.touch_manager.touch_menu(cft.touch_btn_number_4.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_ct_primary_curr_1, cfr.s_ct_primary_curr_2]
		except_addr = ecm.addr_ct_primary_current
		ref_value = roi_keys[1].value[0]
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value)
		
		### CT Primary Current 5 -> 99999 (100000로 변경)
		self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_1.value)
		for i in range(5):
			self.touch_manager.touch_menu(cft.touch_btn_number_0.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_ct_primary_curr_1, cfr.s_ct_primary_curr_2]
		except_addr = ecm.addr_ct_primary_current
		ref_value = roi_keys[1].value[1]
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value)
		### CT Primary Current 초기화(50)
		self.modbus_label.setup_target_initialize(ecm.addr_measurement_setup_access, ecm.addr_ct_primary_current, bit32=50)

		## CT Secondary Current 5-> 10 (11로 변경)
		self.touch_manager.touch_menu(cft.touch_data_view_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_1.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_0.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_ct_secondary_curr_1, cfr.s_ct_secondary_curr_2]
		except_addr = ecm.addr_ct_secondary_current
		ref_value = roi_keys[1].value[1]
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value)
		
		### CT Secondary Current 10-> 5 (4로 변경)
		self.touch_manager.touch_menu(cft.touch_data_view_2.value)
		self.touch_manager.touch_menu(cft.touch_btn_number_4.value)
		self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cfr.s_ct_secondary_curr_1, cfr.s_ct_secondary_curr_2]
		except_addr = ecm.addr_ct_secondary_current
		ref_value = roi_keys[1].value[0]
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ecm.addr_measurement_setup_access.value, ref_value=ref_value)




