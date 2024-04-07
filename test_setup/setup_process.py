import cv2
import easyocr
import numpy as np
from roi_and_answer import RoiAnswer

path123 = r".\image_test\a7300_mea_voltage.png"

clr_location = RoiAnswer()
measurement, mea_voltage = clr_location.color_location()


class SetupProcess:
    
    # 색 감 비교 코드
    def meas_vol_test(self, path123):
        image = cv2.imread(path123)

        def color_detection(a, b, c, d, R, G, B):
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            x, y, w, h = a, b, c, d 
            selected_area = image_rgb[y:y+h, x:x+w]
            average_color = np.mean(selected_area, axis=(0, 1))
            target_color = np.array([R, G, B])
            color_difference = np.linalg.norm(average_color - target_color)
            return color_difference

        color_result1 = color_detection(*measurement)
        color_result2 = color_detection(*mea_voltage)
        
        print(color_result1)
        print(color_result2)

        # if color_result1 < 5 and color_result2 < 5:
        #     cut_voltage_image = self.cut_image(image, 0.25, 1, 0.2, 1)
        #     ocr_error, right_error = self.measurement_voltage_uitest(cut_voltage_image)
        #     if not ocr_error and not right_error:
        #         print("pass")
        #     else:
        #         print("Fail")
        # else:
        #     print("fail")
            
    def meas_cur_test(self):
        #숫자 0 인식이 안됨 개선 필요
        image = cv2.imread(path123)

        def color_detection(a, b, c, d, R, G, B):
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            x, y, w, h = a, b, c, d 
            selected_area = image_rgb[y:y+h, x:x+w]
            average_color = np.mean(selected_area, axis=(0, 1))
            target_color = np.array([R, G, B])
            color_difference = np.linalg.norm(average_color - target_color)
            return color_difference

        color_result1 = color_detection(5, 70, 10, 10, 47, 180, 139)
        color_result2 = color_detection(110, 170, 10, 10, 255, 255, 255)

        if color_result1 < 5 and color_result2 < 5:
            cut_current_image = self.cut_image(image, 0.25, 1, 0.2, 1)
            ocr_error, right_error = self.measurement_currnet_uitest(cut_current_image)
            if not ocr_error and not right_error:
                print("pass")
            else:
                print("Fail")
        else:
            print("fail")
            
            
test002 = SetupProcess()
tt = test002.meas_vol_test(path123)