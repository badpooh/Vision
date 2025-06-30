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

	def setup_ocr_process(self, base_save_path, search_pattern, roi_keys, except_address, access_address, ref_value, template_path, roi_mask, modbus_ref, ref_select=0, refresh=None, coordinates=None, modbus_unit=None):
		sm_condition = False
		"""
		Args:
			base_save_path (str): 결과 저장 디렉토리
			search_pattern (str): 스크린샷 파일 검색 패턴
			roi_keys (list): ROI 키 (길이 2 이상 가정)
			except_address (Enum): 검사에서 제외할 단일 주소 (ex: ecm.addr_wiring)
			access_address (tuple): 측정 접근 주소 (ex: (6000,1))
			template_path: AccuraSM 정답 png 파일
			roi_mask: 
			modbus_ref: 
			ref_select: default=0, List=1
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

		if ref_select == 0:
			ref_title_1 = roi_keys[1].value[1][0]
			ref_title_2 = roi_keys[1].value[1][1]
		elif ref_select == 1:
			ref_title_1 = list(roi_keys[1].value[1])[0]
			ref_title_2 = list(roi_keys[1].value[1])[1]
		elif ref_select == 2:
			ref_title_1 = roi_keys[1].value[1][1]
			ref_title_2 = roi_keys[1].value[1][2]
		
		if roi_keys[1] == ConfigROI.s_primary_reference_vol_3:
			parts = ref_title_1.split(',')
			numeric_part_with_space = parts[0]
			ref_title_1 = numeric_part_with_space.strip()

			parts2 = ref_title_2.split(',')
			numeric_part_with_space2 = parts2[0]
			ref_title_2 = numeric_part_with_space2.strip()

			parts3 = reference_value.split(',')
			numeric_part_with_space3 = parts3[0]
			reference_value = numeric_part_with_space3.strip()

			ocr_1 = ocr_results[1]
			parts4 = ocr_1.split(',')
			numeric_part_with_space4 = parts4[0]
			ocr_1 = numeric_part_with_space4.strip()
			ocr_results[1] = ocr_1

		if roi_keys[1] == ConfigROI.s_primary_reference_vol_4:
			parts = ref_title_1.split(',')
			numeric_part_with_space = parts[-1]
			ref_title_1 = numeric_part_with_space.strip()

			parts2 = ref_title_2.split(',')
			numeric_part_with_space2 = parts2[-1]
			ref_title_2 = numeric_part_with_space2.strip()

			parts3 = reference_value.split(',')
			numeric_part_with_space3 = parts3[-1]
			reference_value = numeric_part_with_space3.strip()

			ocr_1 = ocr_results[1]
			parts4 = ocr_1.split(',')
			numeric_part_with_space4 = parts4[-1]
			ocr_1 = numeric_part_with_space4.strip()
			ocr_results[1] = ocr_1
			print(ocr_results[1])
			
		if self.accruasm_state == 2 and refresh == 'event':
			self.autogui_manager.m_s_event_refresh(image_path, base_save_path, compare_title)
			time.sleep(2.0)
			sm_res, sm_condition = self.autogui_manager.find_and_click(template_path, image_path, base_save_path, compare_title, roi_mask=roi_mask)

		elif self.accruasm_state == 2:
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
			sm_condition = sm_condition,
			modbus_ref=modbus_ref,
			modbus_unit=modbus_unit,
			ref_select = ref_select,
			)
		self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result, title)
		time.sleep(0.5)

	def config_setup_action(self,
                       main_menu=None,
                       side_menu=None,
                       data_view=None,
                       password=None,
                       popup_btn=None,
                       number_input=None,
                       apply_btn=True,
                       roi_keys=None,
                       except_addr=None,
					   access_address=None,
                       ref_value=None,
					   modbus_ref=None,
					   modbus_unit=None,
                       template_path=None,
                       roi_mask=None,
                       search_pattern=None,
                       base_save_path=None,
					   refresh=None,
					   ref_select=0,
					   key_type=None,
                       title_desc=None):
		"""
		예시 인자:
		- main_menu: ConfigTouch.touch_main_menu_1.value
		- side_menu: ConfigTouch.touch_side_menu_1.value
		- data_view: ConfigTouch.touch_data_view_1.value
		- password: True/False => 터치 패스워드
		- popup_btn: ConfigTouch.touch_btn_popup_2.value
		- number_input: '100000' (문자열)
		- apply_btn: True/False
		- roi_keys, except_addr, ref_value, template_path, roi_mask => setup_ocr_process에 필요
		- search_pattern, base_save_path => setup_ocr_process에 필요
		- ref_select: default=0, List=1
		- title_desc => 임의의 식별자 (setup_ocr_process 호출 시 구분)
		"""
		if main_menu is not None:
			self.touch_manager.touch_menu(main_menu)
		if side_menu is not None:
			self.touch_manager.touch_menu(side_menu)
		if data_view is not None:
			self.touch_manager.touch_menu(data_view)

		if password:
			self.touch_manager.touch_password() 

		if popup_btn is not None:
			self.touch_manager.touch_menu(popup_btn)
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)

		if number_input is not None:
			self.touch_manager.input_number(number_input, key_type=key_type)
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)

		if apply_btn:
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)

		if (roi_keys and except_addr and access_address and ref_value and template_path and roi_mask
			and base_save_path and search_pattern):
			self.setup_ocr_process(
				base_save_path,
				search_pattern,
				roi_keys=roi_keys,
				except_address=except_addr,
				access_address=access_address,
				ref_value=ref_value,
				template_path=template_path,
				roi_mask=roi_mask,
				refresh=refresh,
				modbus_ref=modbus_ref,
				modbus_unit=modbus_unit,
				ref_select=ref_select
			)
		else:
			print(f"[DEBUG] Not calling setup_ocr_process for {title_desc} because some param is missing.")

	def setup_m_s_meas_all(self, base_save_path, search_pattern):
		self.setup_meter_s_m_vol(base_save_path, search_pattern)
		self.setup_meter_s_m_curr(base_save_path, search_pattern)
		self.m_s_meas_demand(base_save_path, search_pattern)
		self.m_s_meas_power(base_save_path, search_pattern)

	def setup_meter_s_m_vol(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start()

		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### wiring -> Delta
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_wiring_1, ConfigROI.s_wiring_2],
			except_addr=ConfigMap.addr_wiring,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_wiring_2.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_wiring_2.value[1]['Delta'],
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### wiring -> Wye
		self.config_setup_action(
			main_menu=None,
			side_menu=None, 
			data_view=ConfigTouch.touch_data_view_1.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_wiring_1, ConfigROI.s_wiring_2],
			except_addr=ConfigMap.addr_wiring,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_wiring_2.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_wiring_2.value[1]['Wye'],
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### min.meas.secondary l-n volt 5-> 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=False,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_sec_ln_vol_1, ConfigROI.s_min_meas_sec_ln_vol_2],
			except_addr=ConfigMap.addr_min_measured_secondary_ln_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][0],
			modbus_ref=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][0],
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### min.meas.secondary l-n volt 0-> 11
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=False,
			popup_btn=None,
			number_input='11',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_sec_ln_vol_1, ConfigROI.s_min_meas_sec_ln_vol_2],
			except_addr=ConfigMap.addr_min_measured_secondary_ln_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][1],
			modbus_ref=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_min_measured_secondary_ln_voltage, bit16=5)

		### VT Primary L-L Voltage 49
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=False,
			popup_btn=None,
			number_input='49',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_primary_ll_vol_1, ConfigROI.s_vt_primary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_primary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_vt_primary_ll_vol_2.value[1][0],
			modbus_ref=ConfigROI.s_vt_primary_ll_vol_2.value[1][0],
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### VT Primary L-L Voltage 1000000
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=False,
			popup_btn=None,
			number_input='1000000',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_primary_ll_vol_1, ConfigROI.s_vt_primary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_primary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_vt_primary_ll_vol_2.value[1][1],
			modbus_ref=ConfigROI.s_vt_primary_ll_vol_2.value[1][1],
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_vt_primary_ll_voltage, bit32=1900)

		### VT Secondary L-L Voltage 49
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=False,
			popup_btn=None,
			number_input='49',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_secondary_ll_vol_1, ConfigROI.s_vt_secondary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_secondary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_vt_secondary_ll_vol_2.value[1][0],
			modbus_ref=ConfigROI.s_vt_secondary_ll_vol_2.value[1][0],
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### VT Secondary L-L Voltage 221
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=False,
			popup_btn=None,
			number_input='221',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_secondary_ll_vol_1, ConfigROI.s_vt_secondary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_secondary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_vt_secondary_ll_vol_2.value[1][1],
			modbus_ref=ConfigROI.s_vt_secondary_ll_vol_2.value[1][1],
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### VT Secondary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_vt_secondary_ll_voltage, bit16=1900)

		### Primary Reference Voltage L-L -> L-N
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_ref_ln.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_3],
			except_addr=ConfigMap.addr_reference_voltage_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_primary_reference_vol_3.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_primary_reference_vol_3.value[1]['Line-to-Neutral, 190.0'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Primary Reference Voltage L-N -> L-L
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_ref_ll.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_3],
			except_addr=ConfigMap.addr_reference_voltage_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_primary_reference_vol_3.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_primary_reference_vol_3.value[1]['Line-to-Line, 190.0'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Primary Reference Voltage 49
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=None,
			number_input='49', key_type='ref',
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_4],
			except_addr=ConfigMap.addr_reference_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_primary_reference_vol_4.value[1][0],
			ref_select=1,
			modbus_ref=ConfigROI.s_primary_reference_vol_4.value[1][0],
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Primary Reference Voltage 1000000
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=None,
			number_input='1000000', key_type='ref',
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_4],
			except_addr=ConfigMap.addr_reference_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_primary_reference_vol_4.value[1][1],
			ref_select=1,
			modbus_ref=ConfigROI.s_primary_reference_vol_4.value[1][1],
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		###  Primary Reference Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_reference_voltage, bit32=1900)

		### Sliding Reference Voltage Disable -> Enable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sliding_reference_vol_1, ConfigROI.s_sliding_reference_vol_2],
			except_addr=ConfigMap.addr_sliding_reference_voltage_type,
			access_address=ConfigMap.addr_sliding_reference_voltage_setup_access.value,
			ref_value=list(ConfigROI.s_sliding_reference_vol_2.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_sliding_reference_vol_2.value[1]['Enable'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_sliding_reference_voltage.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Sliding Reference Voltage Enable -> Disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sliding_reference_vol_1, ConfigROI.s_sliding_reference_vol_2],
			except_addr=ConfigMap.addr_sliding_reference_voltage_type,
			access_address=ConfigMap.addr_sliding_reference_voltage_setup_access.value,
			ref_value=list(ConfigROI.s_sliding_reference_vol_2.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_sliding_reference_vol_2.value[1]['Disable'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_sliding_reference_voltage.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Rotating Sequence Positive -> Negative
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_7.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rotation_sequence_1, ConfigROI.s_rotation_sequence_2],
			except_addr=ConfigMap.addr_rotating_sequence,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_rotation_sequence_2.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_rotation_sequence_2.value[1]['Negative'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_rotating_sequence.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Rotating Sequence Negative -> Positive
		self.config_setup_action(
			main_menu=None, 
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_7.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rotation_sequence_1, ConfigROI.s_rotation_sequence_2],
			except_addr=ConfigMap.addr_rotating_sequence,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_rotation_sequence_2.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_rotation_sequence_2.value[1]['Positive'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_rotating_sequence.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

	def setup_meter_s_m_curr(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start()
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### CT Primary Current 50 -> 5 (4로 변경)
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2],
			except_addr=ConfigMap.addr_ct_primary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_ct_primary_curr_2.value[1][0],
			modbus_ref=ConfigROI.s_ct_primary_curr_2.value[1][0],
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,)
		
		### CT Primary Current 5 -> 99999 (100000로 변경) ---> 여기 부터 변경 필요
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='100000',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2],
			except_addr=ConfigMap.addr_ct_primary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_ct_primary_curr_2.value[1][1],
			modbus_unit=None,
			modbus_ref=ConfigROI.s_ct_primary_curr_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### CT Primary Current 초기화(50)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_ct_primary_current, bit32=50)

		## CT Secondary Current 5-> 10 (11로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='11',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_secondary_curr_1, ConfigROI.s_ct_secondary_curr_2],
			except_addr=ConfigMap.addr_ct_secondary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_ct_secondary_curr_2.value[1][1],
			modbus_ref=ConfigROI.s_ct_secondary_curr_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### CT Secondary Current 10-> 5 (4로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_secondary_curr_1, ConfigROI.s_ct_secondary_curr_2],
			except_addr=ConfigMap.addr_ct_secondary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_ct_secondary_curr_2.value[1][0],
			modbus_ref=ConfigROI.s_ct_secondary_curr_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Reference Current 50 > 5 (4로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_reference_curr_1, ConfigROI.s_reference_curr_2],
			except_addr=ConfigMap.addr_reference_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_reference_curr_2.value[1][0],
			modbus_ref=ConfigROI.s_reference_curr_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_reference_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Reference Current 50 > 99999 (100000로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='100000',
			apply_btn=True,
			roi_keys=[ConfigROI.s_reference_curr_1, ConfigROI.s_reference_curr_2],
			except_addr=ConfigMap.addr_reference_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_reference_curr_2.value[1][1],
			modbus_ref=ConfigROI.s_reference_curr_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_reference_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### Reference Current 초기화(50)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_reference_current, bit32=50)
		
		### min measured current 5 > 0 (0으로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_curr_1, ConfigROI.s_min_meas_curr_2],
			except_addr=ConfigMap.addr_min_measured_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_min_meas_curr_2.value[1][0],
			modbus_ref=ConfigROI.s_min_meas_curr_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### min measured current 0 > 100 (101으로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='101',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_curr_1, ConfigROI.s_min_meas_curr_2],
			except_addr=ConfigMap.addr_min_measured_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_min_meas_curr_2.value[1][1],
			modbus_ref=ConfigROI.s_min_meas_curr_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### min measured current 초기화(5)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_min_measured_current, bit16=5)
		
		### tdd reference selection / peak demand > tdd nominal
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_tdd_reference_selection_1, ConfigROI.s_tdd_reference_selection_2],
			except_addr=ConfigMap.addr_tdd_reference,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_tdd_reference_selection_2.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_tdd_reference_selection_2.value[1]['TDD Nominal Current'],
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_tdd_reference_selection.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### tdd reference selection / tdd nominal > peak demand
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_tdd_reference_selection_1, ConfigROI.s_tdd_reference_selection_2],
			except_addr=ConfigMap.addr_tdd_reference,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_tdd_reference_selection_2.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_tdd_reference_selection_2.value[1]['Peak Demand Current'],
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_tdd_reference_selection.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### tdd nominal current 0 > 1 (reference current 체크 해제 후 0)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_ref_curr.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2]
		except_addr = ConfigMap.addr_nominal_tdd_current
		ref_value = roi_keys[1].value[1][1]
		ref_select=2
		modbus_ref = ref_value
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, ref_select=ref_select, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

		### tdd nominal current 1 > 99999 (100000으로 변경)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_1.value)
		for i in range(5):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2]
		except_addr = ConfigMap.addr_nominal_tdd_current
		ref_value = roi_keys[1].value[1][2]
		ref_select=2
		modbus_ref = ref_value
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, ref_select=ref_select, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

		### tdd nominal current 9999 > 0 (reference current로 변경)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_ref_curr.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2]
		except_addr = ConfigMap.addr_nominal_tdd_current
		ref_value = roi_keys[1].value[1][0]
		ref_select=0
		modbus_ref = ref_value
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, ref_value=ref_value, ref_select=ref_select, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

	def m_s_meas_demand(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### Sub-interval time 15 > 1 (input 0)
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sub_interval_time_1, ConfigROI.s_sub_interval_time_2],
			except_addr=ConfigMap.addr_sub_interval_time,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_sub_interval_time_2.value[1][0],
			modbus_ref=ConfigROI.s_sub_interval_time_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_subinterval_time.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sub-interval time 1 > 60 (input 61)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='61',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sub_interval_time_1, ConfigROI.s_sub_interval_time_2],
			except_addr=ConfigMap.addr_sub_interval_time,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_sub_interval_time_2.value[1][1],
			modbus_ref=ConfigROI.s_sub_interval_time_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_subinterval_time.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### min measured current 초기화(15)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_sub_interval_time, bit16=15)
		
		### Number of Sub-Intervals 1 > 12 (input 13)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='61',
			apply_btn=True,
			roi_keys=[ConfigROI.s_number_of_sub_intervals_1, ConfigROI.s_number_of_sub_intervals_2],
			except_addr=ConfigMap.addr_num_of_sub_interval,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_number_of_sub_intervals_2.value[1][1],
			modbus_ref=ConfigROI.s_number_of_sub_intervals_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_number_of_subintervals.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Number of Sub-Intervals 12 > 1 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_number_of_sub_intervals_1, ConfigROI.s_number_of_sub_intervals_2],
			except_addr=ConfigMap.addr_num_of_sub_interval,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_number_of_sub_intervals_2.value[1][0],
			modbus_ref=ConfigROI.s_number_of_sub_intervals_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_number_of_subintervals.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Power Type 0 > 1 (input 1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_power_type_1, ConfigROI.s_demand_power_type_2],
			except_addr=ConfigMap.addr_demand_power_type,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_demand_power_type_2.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_demand_power_type_2.value[1]['Net'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_power_type.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Power Type 1 > 0 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_power_type_1, ConfigROI.s_demand_power_type_2],
			except_addr=ConfigMap.addr_demand_power_type,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_demand_power_type_2.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_demand_power_type_2.value[1]['Received'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_power_type.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Sync Mode 0 > 1 (input 1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_sync_mode_1, ConfigROI.s_demand_sync_mode_2],
			except_addr=ConfigMap.addr_demand_sync_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_demand_sync_mode_2.value[1])[1],
			ref_select=1,
			modbus_ref=ConfigROI.s_demand_sync_mode_2.value[1]['Manual Sync'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_sync_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Sync Mode 1 > 0 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_sync_mode_1, ConfigROI.s_demand_sync_mode_2],
			except_addr=ConfigMap.addr_demand_sync_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=list(ConfigROI.s_demand_sync_mode_2.value[1])[0],
			ref_select=1,
			modbus_ref=ConfigROI.s_demand_sync_mode_2.value[1]['Hourly Auto Sync'],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_sync_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Thermal Response Index 90 > 0 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_thermal_response_index_1, ConfigROI.s_thermal_response_index_2],
			except_addr=ConfigMap.addr_thermal_response_index,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_thermal_response_index_2.value[1][0],
			modbus_ref=ConfigROI.s_thermal_response_index_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_thermal_response_index.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Thermal Response Index 0 > 100 (input 101)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=None,
			number_input='101',
			apply_btn=True,
			roi_keys=[ConfigROI.s_thermal_response_index_1, ConfigROI.s_thermal_response_index_2],
			except_addr=ConfigMap.addr_thermal_response_index,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_thermal_response_index_2.value[1][1],
			modbus_ref=ConfigROI.s_thermal_response_index_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_thermal_response_index.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### Thermal Response Index 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_thermal_response_index, bit16=90)

	def m_s_meas_power(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### Phase Power Calculation 1 > 0 (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_4.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_phase_power_calculation_1, ConfigROI.s_phase_power_calculation_2],
			except_addr=ConfigMap.addr_phase_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_phase_power_calculation_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_phase_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Phase Power Calculation 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_phase_power_calculation_1, ConfigROI.s_phase_power_calculation_2],
			except_addr=ConfigMap.addr_phase_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_phase_power_calculation_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_phase_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Total Power Calculation 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_total_power_calculation_1, ConfigROI.s_total_power_calculation_2],
			except_addr=ConfigMap.addr_total_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_total_power_calculation_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_total_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Total Power Calculation 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_total_power_calculation_1, ConfigROI.s_total_power_calculation_2],
			except_addr=ConfigMap.addr_total_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_total_power_calculation_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_total_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Sign 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_sign_1, ConfigROI.s_pf_sign_2],
			except_addr=ConfigMap.addr_pf_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_pf_sign_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Sign 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_sign_1, ConfigROI.s_pf_sign_2],
			except_addr=ConfigMap.addr_pf_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_pf_sign_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Value at No-Load 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_value_at_noload_1, ConfigROI.s_pf_value_at_noload_2],
			except_addr=ConfigMap.addr_pf_value_at_no_load,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_pf_value_at_noload_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_value_at_noload.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Value at No-Load 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_value_at_noload_1, ConfigROI.s_pf_value_at_noload_2],
			except_addr=ConfigMap.addr_pf_value_at_no_load,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_pf_value_at_noload_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_value_at_noload.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Reactive Power Sign 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_reactive_power_sign_1, ConfigROI.s_reactive_power_sign_2],
			except_addr=ConfigMap.addr_reactive_power_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_reactive_power_sign_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_reactive_power_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Reactive Power Sign 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_reactive_power_sign_1, ConfigROI.s_reactive_power_sign_2],
			except_addr=ConfigMap.addr_reactive_power_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			ref_value=ConfigROI.s_reactive_power_sign_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_reactive_power_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
	
	def setup_m_s_event_all(self, base_save_path, search_pattern):
		self.m_s_event_dip(self, base_save_path, search_pattern)
		self.m_s_event_swell(self, base_save_path, search_pattern)
		self.m_s_event_pq_curve(self, base_save_path, search_pattern)
	
	def m_s_event_dip(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### Dip Trigger Disable > Enable (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_trigger_1, ConfigROI.s_dip_trigger_2],
			except_addr=ConfigMap.addr_dip,
			access_address=ConfigMap.addr_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_trigger_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip Trigger Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_trigger_1, ConfigROI.s_dip_trigger_2],
			except_addr=ConfigMap.addr_dip,
			access_address=ConfigMap.addr_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_trigger_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip Threshold 90 > 10 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_threshold_1, ConfigROI.s_dip_threshold_2],
			except_addr=ConfigMap.addr_dip_threshold,
			access_address=ConfigMap.addr_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_threshold_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip Threshold 10 > 99 (input 100)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='100',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_threshold_1, ConfigROI.s_dip_threshold_2],
			except_addr=ConfigMap.addr_dip_threshold,
			access_address=ConfigMap.addr_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_threshold_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### min measured current 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_dip_setup_access, ConfigMap.addr_dip_threshold, bit16=900)
		
		### Dip hysteresis 2 > 1 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_hysteresis_1, ConfigROI.s_dip_hysteresis_2],
			except_addr=ConfigMap.addr_dip_hysteresis,
			access_address=ConfigMap.addr_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_hysteresis_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip hysteresis 1 > 99 (input 100)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='100',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_hysteresis_1, ConfigROI.s_dip_hysteresis_2],
			except_addr=ConfigMap.addr_dip_hysteresis,
			access_address=ConfigMap.addr_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_hysteresis_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### min measured current 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_dip_setup_access, ConfigMap.addr_dip_hysteresis, bit16=20)

		### 3-Phase Dip Disable > Enable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_3phase_dip_1, ConfigROI.s_dip_3phase_dip_2],
			except_addr=ConfigMap.addr_3phase_dip,
			access_address=ConfigMap.addr_3phase_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_3phase_dip_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_3dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### 3-Phase Dip Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_3phase_dip_1, ConfigROI.s_dip_3phase_dip_2],
			except_addr=ConfigMap.addr_3phase_dip,
			access_address=ConfigMap.addr_3phase_dip_setup_access.value,
			ref_value=ConfigROI.s_dip_3phase_dip_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_3dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
	def m_s_event_swell(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()
		
		### Swell Trigger Disable > Enable (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_trigger_1, ConfigROI.s_swell_trigger_2],
			except_addr=ConfigMap.addr_swell,
			access_address=ConfigMap.addr_swell_setup_access.value,
			ref_value=ConfigROI.s_swell_trigger_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Trigger Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_trigger_1, ConfigROI.s_swell_trigger_2],
			except_addr=ConfigMap.addr_swell,
			access_address=ConfigMap.addr_swell_setup_access.value,
			ref_value=ConfigROI.s_swell_trigger_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Threshold 110 > 101 (input 100.9)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='100.9',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_threshold_1, ConfigROI.s_swell_threshold_2],
			except_addr=ConfigMap.addr_swell_threshold,
			access_address=ConfigMap.addr_swell_setup_access.value,
			ref_value=ConfigROI.s_swell_threshold_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Threshold 101 > 999 (input 999.1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='999.1',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_threshold_1, ConfigROI.s_swell_threshold_2],
			except_addr=ConfigMap.addr_swell_threshold,
			access_address=ConfigMap.addr_swell_setup_access.value,
			ref_value=ConfigROI.s_swell_trigger_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### Swell Threshold 초기화(110)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_swell_setup_access, ConfigMap.addr_swell_threshold, bit16=1100)

		### Swell Hysteresis 2 > 1 (input 0.9)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='0.9',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_hysteresis_1, ConfigROI.s_swell_hysteresis_2],
			except_addr=ConfigMap.addr_swell_hysteresis,
			access_address=ConfigMap.addr_swell_setup_access.value,
			ref_value=ConfigROI.s_swell_hysteresis_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Hysteresis 1 > 99 (input 99.1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='99.1',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_hysteresis_1, ConfigROI.s_swell_hysteresis_2],
			except_addr=ConfigMap.addr_swell_hysteresis,
			access_address=ConfigMap.addr_swell_setup_access.value,
			ref_value=ConfigROI.s_swell_hysteresis_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### Swell Hysteresis 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_swell_setup_access, ConfigMap.addr_swell_hysteresis, bit16=20)

	def m_s_event_pq_curve(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()
		
		### SEMI F47-0706 Disable > Enable (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_semi_1, ConfigROI.s_pq_curve_semi_2],
			except_addr=ConfigMap.addr_semi,
			access_address=ConfigMap.addr_semi_event_setup_access.value,
			ref_value=ConfigROI.s_pq_curve_semi_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_semi.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### SEMI F47-0706 Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_semi_1, ConfigROI.s_pq_curve_semi_2],
			except_addr=ConfigMap.addr_semi,
			access_address=ConfigMap.addr_semi_event_setup_access.value,
			ref_value=ConfigROI.s_pq_curve_semi_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_semi.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### IEC 61000-4-11/34 Class 3 Disable > Enable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_iec_1, ConfigROI.s_pq_curve_iec_2],
			except_addr=ConfigMap.addr_iec,
			access_address=ConfigMap.addr_iec_event_setup_access.value,
			ref_value=ConfigROI.s_pq_curve_iec_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_iec.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### IEC 61000-4-11/34 Class 3 Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_iec_1, ConfigROI.s_pq_curve_iec_2],
			except_addr=ConfigMap.addr_iec,
			access_address=ConfigMap.addr_iec_event_setup_access.value,
			ref_value=ConfigROI.s_pq_curve_iec_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_iec.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### ITIC Disable > Enable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_itic_1, ConfigROI.s_pq_curve_itic_2],
			except_addr=ConfigMap.addr_itic,
			access_address=ConfigMap.addr_itic_event_setup_access.value,
			ref_value=ConfigROI.s_pq_curve_itic_2.value[1][1],
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_itic.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### ITIC Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_itic_1, ConfigROI.s_pq_curve_itic_2],
			except_addr=ConfigMap.addr_itic,
			access_address=ConfigMap.addr_itic_event_setup_access.value,
			ref_value=ConfigROI.s_pq_curve_itic_2.value[1][0],
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_itic.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
	


