import time
from function.func_ocr import OCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation

from config.config_touch import ConfigTouch as cft
from config.config_roi import ConfigROI as cr
from config.config_map import ConfigModbusMap as ecm
from config.config_map import ConfigInitialValue as civ

image_directory = r"\\10.10.20.30\screenshot"
ocr_func = OCRManager()

class SetupTest:
     
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()
	eval_manager = Evaluation()

	def __init__(self):
		pass

	def setup_ocr_process(self, base_save_path, search_pattern, roi_keys, except_address, reference_value, compare_title, access_address, target_address, ref_title_1, ref_title_2):
		"""
		Args:
			savebase_save_path (str): 결과를 저장할 디렉터리 경로
			search_pattern (str): 스크린샷 파일 등을 검색할 패턴 (예: glob 형태)
			roi_keys (list): ROI 정보가 담긴 리스트 (예: [cr.s_wiring_1, cr.s_wiring_2])
			excluded_addr (Enum): 검사에서 제외할 Modbus 주소 Enum 멤버 (예: {ecm.addr_wiring})
			reference_value (str): 설정 시 비교할 값 (예: cr.s_wiring_2.value[0])
			compare_title (str): OCR 결과에서 확인할 키워드 (예: 'Wiring'이나 cr.s_min_meas_sec_ln_vol_1.value)
			access_address (tuple): 접근 주소 (예: ecm.addr_measurement_setup_access.value → (6000, 1))
			target_address (tuple): 실제 체크할 주소 (예: ecm.addr_wiring.value → (6001, 1))
			ref_title_1 (str): 추가 비교에 사용될 텍스트 1 (예: cr.s_wiring_2.value[0])
			ref_title_2 (str): 추가 비교에 사용될 텍스트 2 (예: cr.s_wiring_2.value[1])

		Returns:
			None
		"""
		self.touch_manager.screenshot()
		image_path = self.eval_manager.load_image_file(search_pattern)
		ocr_results = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
		except_addr = {except_address}
		setup_result, modbus_result, overall_result = self.eval_manager.eval_setup_test(
			ocr_res=ocr_results,
			setup_ref=reference_value,
			title=compare_title,
			ecm_access_address=access_address,
			ecm_address=target_address,
			setup_ref_title_1=ref_title_1,
			setup_ref_title_2=ref_title_2,
			except_addr=except_addr
			)
		self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result)
		time.sleep(0.5)
		
	def setup_meas_vol(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start()
		### wiring -> Delta
		# self.touch_manager.btn_front_meter()
		# self.touch_manager.btn_front_setup()
		# self.touch_manager.touch_menu(cft.touch_main_menu_1.value)
		# self.touch_manager.touch_menu(cft.touch_side_menu_1.value)
		# self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		# self.touch_manager.touch_password()
		# self.touch_manager.touch_menu(cft.touch_btn_popup_2.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		roi_keys = [cr.s_wiring_1, cr.s_wiring_2]
		except_addr = ecm.addr_wiring
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, cr.s_wiring_2.value[1], cr.s_wiring_1.value[0], ecm.addr_measurement_setup_access.value, ecm.addr_wiring.value, cr.s_wiring_2.value[0], cr.s_wiring_2.value[1])
		

		# ### wiring -> Wye
		# self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_1.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		# self.touch_manager.screenshot()
		# image_path = self.eval_manager.load_image_file(search_pattern)
		# roi_keys = [cr.s_wiring_1, cr.s_wiring_2]
		# ocr_results = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
		# except_addr = {ecm.addr_wiring}
		# setup_ref = cr.s_wiring_2.value[0]
		# setup_result, modbus_result, overall_result = self.eval_manager.eval_setup_test(ocr_res=ocr_results, setup_ref=setup_ref, title='Wiring', ecm_access_address=ecm.addr_measurement_setup_access.value, ecm_address=ecm.addr_wiring.value, setup_ref_title_1=cr.s_wiring_2.value[0], setup_ref_title_2=cr.s_wiring_2.value[1], except_addr=except_addr)
		# self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result)
		# time.sleep(0.5)

		# ### min.meas.secondary l-n volt
		# self.touch_manager.touch_menu(cft.touch_data_view_2.value)
		# self.touch_manager.touch_menu(cft.touch_btn_number_0.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		# self.touch_manager.screenshot()
		# image_path = self.eval_manager.load_image_file(search_pattern)
		# roi_keys = [cr.s_min_meas_sec_ln_vol_1, cr.s_min_meas_sec_ln_vol_2]
		# ocr_results = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
		# except_addr = {ecm.addr_min_measured_secondary_ln_voltage}
		# setup_ref = cr.s_min_meas_sec_ln_vol_2.value[0]
		# setup_result, modbus_result, overall_result = self.eval_manager.eval_setup_test(ocr_res=ocr_results, setup_ref=setup_ref, title=cr.s_min_meas_sec_ln_vol_1.value[0], ecm_access_address=ecm.addr_measurement_setup_access.value, ecm_address=ecm.addr_min_measured_secondary_ln_voltage.value, setup_ref_title_1=cr.s_min_meas_sec_ln_vol_2.value[0], setup_ref_title_2=cr.s_min_meas_sec_ln_vol_2.value[1], except_addr=except_addr)
		# self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result)
		# time.sleep(0.5)

		# self.touch_manager.touch_menu(cft.touch_data_view_2.value)
		# for i in range(2):
		# 	self.touch_manager.touch_menu(cft.touch_btn_number_1.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		# roi_keys = [cr.s_min_meas_sec_ln_vol_1, cr.s_min_meas_sec_ln_vol_2]
		# ocr_results = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
		# except_addr = {ecm.addr_min_measured_secondary_ln_voltage}
		# setup_ref = cr.s_min_meas_sec_ln_vol_2.value[0]
		# setup_result, modbus_result, overall_result = self.eval_manager.eval_setup_test(ocr_res=ocr_results, setup_ref=setup_ref, title=cr.s_min_meas_sec_ln_vol_1.value[0], ecm_access_address=ecm.addr_measurement_setup_access.value, ecm_address=ecm.addr_min_measured_secondary_ln_voltage.value, setup_ref_title_1=cr.s_min_meas_sec_ln_vol_2.value[0], setup_ref_title_2=cr.s_min_meas_sec_ln_vol_2.value[1], except_addr=except_addr)
		# self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result)
		# time.sleep(0.5)



