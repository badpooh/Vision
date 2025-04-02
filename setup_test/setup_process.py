import time
from function.func_ocr import PaddleOCRManager
from function.func_ocr import EasyOCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation
from function.func_autogui import AutoGUI
from PySide6.QtCore import Qt, QObject

from config.config_touch import ConfigTouch
from config.config_roi import ConfigROI
from config.config_map import ConfigMap
from config.config_map import ConfigInitialValue as civ
from config.config_ref import ConfigImgRef

image_directory = r"\\10.10.20.30\screenshot"
paddleocr_func = PaddleOCRManager()
easyocr_func = EasyOCRManager()

class SetupTest(QObject):
     
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()
	eval_manager = Evaluation()
	autogui_manager = AutoGUI()

	def __init__(self):
		super().__init__()
		self.accruasm_state = 2 # 초기 상태 설정

	def on_accurasm_checked(self, state):
		self.accruasm_state = state
		# print(f"SetupProcess: AccuraSM checked={state}")

	def setup_ocr_process(self, base_save_path, search_pattern, roi_keys, except_address, access_address, ref_value, template_path, roi_mask, coordinates=None):
		sm_condition = False
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
		print(self.accruasm_state)
		if self.accruasm_state == 2:
			self.autogui_manager.m_s_meas_refresh(image_path, base_save_path, compare_title)
			time.sleep(2.0)
			sm_res, sm_condition = self.autogui_manager.find_and_click(template_path, image_path, base_save_path, compare_title, roi_mask=roi_mask)
		else:
			sm_res = None
			self.accruasm_state = None
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
		self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_1.value)
		self.touch_manager.touch_password()
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_wiring_1, ConfigROI.s_wiring_2]
		except_addr = ConfigMap.addr_wiring
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_wiring.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		
		### wiring -> Wye
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_wiring_1, ConfigROI.s_wiring_2]
		except_addr = ConfigMap.addr_wiring
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_wiring.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)

		## min.meas.secondary l-n volt 5-> 0
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_min_meas_sec_ln_vol_1, ConfigROI.s_min_meas_sec_ln_vol_2]
		except_addr = ConfigMap.addr_min_measured_secondary_ln_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		
		### min.meas.secondary l-n volt 0-> 11
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		for i in range(2):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_min_meas_sec_ln_vol_1, ConfigROI.s_min_meas_sec_ln_vol_2]
		except_addr = ConfigMap.addr_min_measured_secondary_ln_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### min.meas.secondary l-n volt 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_min_measured_secondary_ln_voltage, bit16=5)

		## VT Primary L-L Voltage 49 --> roi 2번 좌표가 아래로 뒤집어짐? 좌표 확인 필요
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_3.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_9.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_vt_primary_ll_vol_1, ConfigROI.s_vt_primary_ll_vol_2]
		except_addr = ConfigMap.addr_vt_primary_ll_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_vt_primary.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)

		## VT Primary L-L Voltage 1000000
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_3.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_1.value)
		for i in range(6):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_vt_primary_ll_vol_1, ConfigROI.s_vt_primary_ll_vol_2]
		except_addr = ConfigMap.addr_vt_primary_ll_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_vt_primary.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_vt_primary_ll_voltage, bit32=1900)

		### VT Secondary L-L Voltage 49
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_9.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_vt_secondary_ll_vol_1, ConfigROI.s_vt_secondary_ll_vol_2]
		except_addr = ConfigMap.addr_vt_secondary_ll_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_vt_secondary.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### VT Secondary L-L Voltage 221
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_4.value)
		for i in range(2):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_vt_secondary_ll_vol_1, ConfigROI.s_vt_secondary_ll_vol_2]
		except_addr = ConfigMap.addr_vt_secondary_ll_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_vt_secondary.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_vt_secondary_ll_voltage, bit16=1900)

		### Primary Reference Voltage L-L -> L-N
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_5.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_ref_ln.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_2]
		except_addr = ConfigMap.addr_reference_voltage_mode
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### Primary Reference Voltage L-N -> L-L
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_5.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_ref_ll.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_2]
		except_addr = ConfigMap.addr_reference_voltage_mode
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)

		### Primary Reference Voltage 49
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_5.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_ref_num_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_ref_num_9.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_3]
		except_addr = ConfigMap.addr_reference_voltage
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_primary_reference_voltage.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### Primary Reference Voltage 1000000
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_5.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_ref_num_1.value)
		for i in range(6):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_ref_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_3]
		except_addr = ConfigMap.addr_reference_voltage
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_primary_reference_voltage.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_reference_voltage, bit32=1900)

		### Sliding Reference Voltage Disable -> Enable
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_sliding_reference_vol_1, ConfigROI.s_sliding_reference_vol_2]
		except_addr = ConfigMap.addr_sliding_reference_voltage_type
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_sliding_reference_voltage.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_sliding_reference_voltage_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### Sliding Reference Voltage Enable -> Disable
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_sliding_reference_vol_1, ConfigROI.s_sliding_reference_vol_2]
		except_addr = ConfigMap.addr_sliding_reference_voltage_type
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_sliding_reference_voltage.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_sliding_reference_voltage_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)

		### Rotating Sequence Positive -> Negative
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_7.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_rotation_sequence_1, ConfigROI.s_rotation_sequence_1]
		except_addr = ConfigMap.addr_rotating_sequence
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_rotating_sequence.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### Rotating Sequence Negative -> Positive
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_rotation_sequence_1, ConfigROI.s_rotation_sequence_1]
		except_addr = ConfigMap.addr_rotating_sequence
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_rotating_sequence.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)

	def setup_meter_s_m_curr(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		### CT Primary Current 50 -> 5 (4로 변경)
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()
		self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_1.value)
		self.touch_manager.touch_password()
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2]
		except_addr = ConfigMap.addr_ct_primary_current
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_meas_min.value
		roi_mask = ConfigROI.mask_m_s_meas_ct_primary.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		
		### CT Primary Current 5 -> 99999 (100000로 변경) ---> 여기 부터 변경 필요
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_1.value)
		for i in range(5):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2]
		except_addr = ConfigMap.addr_ct_primary_current
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_ct_primary_curr_99999.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		### CT Primary Current 초기화(50)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_ct_primary_current, bit32=50)

		## CT Secondary Current 5-> 10 (11로 변경)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_1.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_ct_secondary_curr_1, ConfigROI.s_ct_secondary_curr_2]
		except_addr = ConfigMap.addr_ct_secondary_current
		ref_value = roi_keys[1].value[1]
		template_path = ConfigImgRef.img_ref_ct_secondary_curr_10.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)
		
		### CT Secondary Current 10-> 5 (4로 변경)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_number_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_ct_secondary_curr_1, ConfigROI.s_ct_secondary_curr_2]
		except_addr = ConfigMap.addr_ct_secondary_current
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_ct_secondary_curr_5.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)

	def setup_meter_s_e_dip(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		### Dip Trigger Disable > Enable 
		# self.touch_manager.btn_front_meter()
		# self.touch_manager.btn_front_setup()
		# self.touch_manager.touch_menu(cft.touch_main_menu_2.value)
		# self.touch_manager.touch_menu(cft.touch_side_menu_1.value)
		# self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		# self.touch_manager.touch_password()
		# self.touch_manager.touch_menu(cft.touch_btn_popup_2.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_dip_trigger_1, ConfigROI.s_dip_trigger_2]
		except_addr = ConfigMap.addr_dip
		ref_value = roi_keys[1].value[0]
		template_path = ConfigImgRef.img_ref_meter_setup_event_max.value
		roi_mask = [9, 51, 248, 72]
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, template_path=template_path, roi_mask=roi_mask)


