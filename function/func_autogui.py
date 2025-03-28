import cv2
import numpy as np
import pyautogui
import time
import os
from function.func_modbus import ConnectionManager
from config.config_ref import ConfigImgRef

### 배율 100% 아닐시 동작 및 이미지 매칭 오류발생

class AutoGUI:

	connect_manager = ConnectionManager()

	def find_and_click(self, template_path, img_path, base_save_path, title, coordinates=None, save_statue=1, click=0):
		self.sm_condition = False
		
		file_name_with_extension = os.path.basename(img_path)  
		ip_to_remove = f"{self.connect_manager.SERVER_IP}_"    
		if file_name_with_extension.startswith(ip_to_remove):
			file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
		else:
			file_name_without_ip = file_name_with_extension

		# 확장자 제거
		image_file_name = os.path.splitext(file_name_without_ip)[0]
		save_path = os.path.join(base_save_path, f'{image_file_name}_{title}.png')
		dest_image_path = os.path.join(base_save_path, file_name_without_ip)

		screenshot = pyautogui.screenshot()
		screenshot = np.array(screenshot)  
		screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  

		template = cv2.imread(template_path, cv2.IMREAD_COLOR)
		h, w, _ = template.shape

		result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

		threshold = 0.8
		top_left = max_loc
		if max_val >= threshold and coordinates:
			w_1, h_1 = coordinates
			center_x = top_left[0] + w_1*w
			center_y = top_left[1] + h_1*h

			pyautogui.moveTo(center_x, center_y, duration=0.5)
			time.sleep(1)
			box_width, box_height = w, h
			screenshot_region = pyautogui.screenshot(region=(top_left[0], top_left[1], box_width, box_height))
			if save_statue == 1:
				screenshot_region.save(save_path)
			else:
				pass
			pyautogui.click()
			sm_res = None

		else:
			box_width, box_height = w, h
			screenshot_region = pyautogui.screenshot(region=(top_left[0], top_left[1], box_width, box_height))
			screenshot_region.save(save_path)

			if max_val >= threshold:
				sm_res = f'PASS_{max_val:.3f}_{title}'
				self.sm_condition = True
			else:
				sm_res = f'FAIL_{max_val:.3f}_{title}'

		print(sm_res)
			
		return sm_res, self.sm_condition

	def m_s_meas_refresh(self, img_path, base_save_path, title):
		print('refresh 함수는 동작?')
		template_path = ConfigImgRef.img_ref_meas_refresh.value
		coordinates = [0.94, 0.48]
		self.find_and_click(template_path, img_path, base_save_path, title, coordinates, save_statue=0, click=1)
