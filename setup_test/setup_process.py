import cv2
import numpy as np
import os, glob
from datetime import datetime
import time

from setup_test.setup_function import TouchManager, ModbusManager, OCRImageManager, Evaluation, ModbusLabels


image_directory = r"\\10.10.20.30\screenshot"


class SetupProcess:
    
    touch_manager = TouchManager()
    modbus_manager = ModbusManager()
    edit_image = OCRImageManager()
    image_uitest = Evaluation()
    modbus_label = ModbusLabels()
    search_pattern = os.path.join(image_directory, './**/*10.10.26.156*.png')
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

        #### 3P4W일때 Wiring 제외하고 모든 설정 ####
    def test_m_m_v(self):
        initial_values = self.modbus_label.read_all_modbus_values()
        time.sleep(1)
        self.touch_manager.menu_touch("main_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("side_menu_1")
        time.sleep(0.6)
        self.touch_manager.menu_touch("data_view_2")
        time.sleep(0.6)
        #### 최소치 1 ####
        self.touch_manager.number_1_touch("btn_number_1")
        time.sleep(0.6)
        change_count = self.modbus_label.display_changes(initial_values)
        if change_count >= 2:
            print("check other address value")
        else:
            self.touch_manager.screenshot()
            time.sleep(0.6)
            image_path = self.load_image_file()
            image = cv2.imread(image_path)
            color_result = self.edit_image.color_detection(image, *self.coords_color["measurement"])
            color_result1 = self.edit_image.color_detection(image, *self.coords_color["mea_voltage"])

            if color_result < 5 and color_result1 < 5:
                cut_voltage_image = self.edit_image.image_cut_custom(image=image_path)
                ocr_error, right_error = self.image_uitest.measurement_voltage_uitest(cut_voltage_image)
                if not ocr_error and not right_error:
                    print("pass")
                else:
                    print("Fail")
            else:
                print("fail")
            pass
        
    
    def load_image_file(self):
        for file_path in glob.glob(self.search_pattern, recursive=True):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            time_diff = abs((self.now - creation_time).total_seconds())
            self.file_time_diff[file_path] = time_diff

        closest_file = min(self.file_time_diff, key=self.file_time_diff.get, default=None)
        normalized_path = os.path.normpath(closest_file)

        print("가장 가까운 시간에 생성된 파일:", normalized_path)

        return normalized_path

    
    def read_setup_mapping(self):
        modbus_results = self.modbus_label.read_all_modbus_values()
        for description, value in modbus_results.items():
            print(f"{description}: {value}")

    # def wiring_test(self):
    #     self.image_path = self.load_image_file()
    #     color_result = self.color_detection(self.image_path, *self.measurement)
    #     color_result1 = self.color_detection(self.image_path, *self.mea_voltage)
        
    #     if color_result < 5 and color_result1 < 5:
    #         cut_voltage_image = self.cut_image(self.image_path, 0.25, 1, 0.2, 1)
    #         ocr_error, right_error = self.measurement_voltage_uitest(cut_voltage_image)
    #         if not ocr_error and not right_error:
    #             print("pass")
    #         else:
    #             print("Fail")
    #     else:
    #         print("fail")
    

    
    
#     # 색 감 비교 코드
#     # def meas_vol_test(self, path123):
#     #     image = cv2.imread(path123)

#     #     def color_detection(a, b, c, d, R, G, B):
#     #         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     #         x, y, w, h = a, b, c, d 
#     #         selected_area = image_rgb[y:y+h, x:x+w]
#     #         average_color = np.mean(selected_area, axis=(0, 1))
#     #         target_color = np.array([R, G, B])
#     #         color_difference = np.linalg.norm(average_color - target_color)
#     #         return color_difference

#     #     color_result1 = color_detection(*measurement)
#     #     color_result2 = color_detection(*mea_voltage)
        
#     #     print(color_result1)
#     #     print(color_result2)

#         # if color_result1 < 5 and color_result2 < 5:
#         #     cut_voltage_image = self.cut_image(image, 0.25, 1, 0.2, 1)
#         #     ocr_error, right_error = self.measurement_voltage_uitest(cut_voltage_image)
#         #     if not ocr_error and not right_error:
#         #         print("pass")
#         #     else:
#         #         print("Fail")
#         # else:
#         #     print("fail")
            
#     def meas_cur_test(self):
#         #숫자 0 인식이 안됨 개선 필요
#         image = cv2.imread(path123)

#         def color_detection(a, b, c, d, R, G, B):
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             x, y, w, h = a, b, c, d 
#             selected_area = image_rgb[y:y+h, x:x+w]
#             average_color = np.mean(selected_area, axis=(0, 1))
#             target_color = np.array([R, G, B])
#             color_difference = np.linalg.norm(average_color - target_color)
#             return color_difference

#         color_result1 = color_detection(5, 70, 10, 10, 47, 180, 139)
#         color_result2 = color_detection(110, 170, 10, 10, 255, 255, 255)

#         if color_result1 < 5 and color_result2 < 5:
#             cut_current_image = self.cut_image(image, 0.25, 1, 0.2, 1)
#             ocr_error, right_error = self.measurement_currnet_uitest(cut_current_image)
#             if not ocr_error and not right_error:
#                 print("pass")
#             else:
#                 print("Fail")
#         else:
#             print("fail")
            
            
# test002 = SetupProcess()
# tt = test002.meas_vol_test(path123)