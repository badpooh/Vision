
from function.func_ocr import OCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels

from config.config_touch import ConfigTouch as cft

image_directory = r"\\10.10.20.30\screenshot"
ocr_func = OCRManager()

class SetupTest:
     
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()

	def __init__(self):
		pass

	def setup_mea_vol(self):
		# self.touch_manager.btn_front_meter()
		# self.touch_manager.btn_front_setup()
		# self.touch_manager.menu_touch(cft.touch_main_menu_1.value)
		# self.touch_manager.menu_touch(cft.touch_side_menu_1.value)
		# self.touch_manager.menu_touch(cft.touch_data_view_1.value)
		self.modbus_label.setup_initialization()
