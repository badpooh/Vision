import cv2
import easyocr
import numpy as np
from itertools import chain

image_path = r"\\10.10.10.11\pnt\nfs\A2500_20240326_165256.png"
# 이미지 불러오기

def cut_image(image, height_ratio_start, height_ratio_end, width_ratio_start, width_ratio_end):
    height, width = image.shape[:2]
    cropped_image = image[int(height*height_ratio_start):int(height*height_ratio_end),
                          int(width*width_ratio_start):int(width*width_ratio_end)]
    resized_image = cv2.resize(cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 이미지 블러 처리 및 선명하게 만들기
    blurred_image = cv2.GaussianBlur(resized_image, (0, 0), 3)
    sharpened_image = cv2.addWeighted(resized_image, 1.5, blurred_image, -0.5, 0)
    return sharpened_image

def voltageLL_uitest(image_path):
    image = cv2.imread(image_path)

    sharpened_image_1 = cut_image(image, 0.229, 1, 0, 0.1875)
    sharpened_image_2 = cut_image(image, 0.26, 0.354, 0.2, 1)
    sharpened_image_3 = cut_image(image, 0.375, 1, 0.212, 0.437)
    
    reader = easyocr.Reader(['en'])
    ocr_results_1 = reader.readtext(sharpened_image_1, detail=0)
    ocr_results_2 = reader.readtext(sharpened_image_2, detail=0)
    ocr_results_3 = reader.readtext(sharpened_image_3, detail=0)

    ocr_right_1 = ["Line-to-Line", "Line-to-Neutral", "LL Fund.", "LN Fund.", "LL THD %", "LN THD %", "Frequency", "Residual"]
    ocr_right_2 = ["Line-to-Line Voltage", "Min", "Max"]
    ocr_right_3 = ["AB", "BC", "CA", "Average"]

    right_set_1 = set(text.strip() for text in ocr_right_1)
    right_set_2 = set(text.strip() for text in ocr_right_2)
    right_set_3 = set(text.strip() for text in ocr_right_3)

    ocr_set_1 = set(result.strip() for result in ocr_results_1)
    ocr_set_2 = set(result.strip() for result in ocr_results_2)
    ocr_set_3 = set(result.strip() for result in ocr_results_3)


    leave_ocr_all = [
    (ocr_set_1 - right_set_1),
    (ocr_set_2 - right_set_2),
    (ocr_set_3 - right_set_3),
    ]
    leave_right_all = [
        (right_set_1 - ocr_set_1),
        (right_set_2 - ocr_set_2),
        (right_set_3 - ocr_set_3),
    ]
    
    ocr_error = list(chain(*leave_ocr_all))
    right_error = list(chain(*leave_right_all))

    # OCR 결과와 매칭되지 않아 남은 단어
    print(f"OCR 결과와 매칭되지 않는 단어들: {ocr_error}")
    print(f"\n정답 중 OCR 결과와 매칭되지 않는 단어들: {right_error}")

    
    
    # cv2.imshow('Image with Size Info', sharpened_image_3)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

voltageLL_uitest(image_path)
# 이미지 보여주기


# 색 감 비교 코드
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# x, y, w, h = 120, 130, 10, 10 
# selected_area = image_rgb[y:y+h, x:x+w]
# average_color = np.mean(selected_area, axis=(0, 1))
# target_color = np.array([255, 255, 255])
# color_difference = np.linalg.norm(average_color - target_color)

# print("Average color of selected area:", average_color)
# print("Difference from target color:", color_difference)