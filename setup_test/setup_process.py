

from function.func_ocr import OCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation

from config.config_touch import ConfigTouch as cft
from config.config_roi import ConfigROI as cr

image_directory = r"\\10.10.20.30\screenshot"
ocr_func = OCRManager()

class SetupTest:
     
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()
	eval_manager = Evaluation()

	def __init__(self):
		pass

	# def ocr_process_setup(self, image_path, roi_keys, ocr_ref, time_keys=None, reset_time=None, base_save_path=None):
	# 	"""
	# 	Args:
	# 		image_path (str): The path to the image file.
	# 		roi_keys (list): List of ROI keys for general OCR processing.
	# 		ocr_ref (str): The OCR type to be selected for evaluation.
	# 		time_keys (list): Min, Max time
	# 		reset_time (time): Min, Max reset time
	# 		img_result (str): image match curculation result
	# 	Returns:
	# 		None
	# 	"""
	# 	ocr_res = None
	# 	ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
	# 		ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.eval_manager.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
	# 			time_results = self.eval_manager.check_time_diff(image=image_path, roi_keys=time_keys, reset_time=reset_time, test_mode=test_mode)
	# 			self.eval_manager.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, time_results=time_results, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)
	# 		else:
	# 			self.eval_manager.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)
	# 	else:
	# 		print("self.test_mode type error")

	# 	return ocr_res

	def setup_mea_vol(self, search_pattern):
		# self.touch_manager.uitest_mode_start()
		self.modbus_label.setup_initialization()
		# self.touch_manager.btn_front_meter()
		# self.touch_manager.btn_front_setup()
		# self.touch_manager.touch_menu(cft.touch_main_menu_1.value)
		# self.touch_manager.touch_menu(cft.touch_side_menu_1.value)
		# self.touch_manager.touch_menu(cft.touch_data_view_1.value)
		# self.touch_manager.touch_password()
		# self.touch_manager.touch_menu(cft.touch_btn_popup_2.value)
		# self.touch_manager.touch_menu(cft.touch_btn_popup_enter.value)
		# self.touch_manager.touch_menu(cft.touch_btn_apply.value)
		self.touch_manager.screenshot()
		image_path = self.eval_manager.load_image_file(search_pattern)
		roi_keys = [cr.s_wiring_1, cr.s_wiring_2]
		ocr_results = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
		target_result = self.eval_manager.eval_setup_test(ocr_res=ocr_results)
		print(target_result)

