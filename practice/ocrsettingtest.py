from unittest import result
import cv2
import easyocr
import numpy as np
from itertools import chain

image_path = r"C:\Users\Jin\Desktop\Company\Rootech\PNT\AutoProgram\image_1\a7300_mea_voltage.png"
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

def measurement_uitest(image):
    # image = cv2.imread(image_th)
    
    reader = easyocr.Reader(['en'])
    ocr_results_1 = reader.readtext(image, detail=0)
    ocr_results_2 = reader.readtext(image)
    
    for result in ocr_results_2:
        bbox, text, prob = result
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        # 이미지에 바운딩 박스 그리기
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

        # 이미지에 텍스트 쓰기 (선택적)
        cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    ocr_right_1 = ["Voltage", "Wiring", "Min. Measured Secondary Voltage [V]", "VT Primary L-L Voltage [V]", "VT Secondary L-L Voltage [V]", "Primary Reference Voltage [V]", "Sliding Reference Voltage", "Rotating Sequence", "3P4W", "5", "190.0", "190.0", "Line-to-Line, 190.0", "Disable", "Positive"]

    right_set_1 = set(text.strip() for text in ocr_right_1)

    ocr_set_1 = set(result.strip() for result in ocr_results_1)


    leave_ocr_all = [
    (ocr_set_1 - right_set_1),
    ]
    leave_right_all = [
        (right_set_1 - ocr_set_1),
    ]
    
    ocr_error = list(chain(*leave_ocr_all))
    right_error = list(chain(*leave_right_all))

    # OCR 결과와 매칭되지 않아 남은 단어
    print(f"OCR 결과와 매칭되지 않는 단어들: {ocr_error}")
    print(f"\n정답 중 OCR 결과와 매칭되지 않는 단어들: {right_error}")
    
    cv2.imshow('Image with Size Info', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return ocr_error

    
    
    

# 이미지 보여주기


# 색 감 비교 코드
image = cv2.imread(image_path)

def color_detection(a, b, c, d, R, G, B):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    x, y, w, h = a, b, c, d 
    # x, y, w, h = 5, 70, 10, 10 
    selected_area = image_rgb[y:y+h, x:x+w]
    average_color = np.mean(selected_area, axis=(0, 1))
    target_color = np.array([R, G, B])
    # target_color = np.array([47, 180, 139])
    color_difference = np.linalg.norm(average_color - target_color)
    # print("Average color of selected area:", average_color)
    # print("Difference from target color:", color_difference)
    return color_difference

color_result1 = color_detection(5, 70, 10, 10, 47, 180, 139)
color_result2 = color_detection(110, 130, 10, 10, 255, 255, 255)
if color_result1 < 10 and color_result2 < 10:
    cut_voltage_image = cut_image(image, 0.25, 1, 0.2, 1)
    last_result = measurement_uitest(cut_voltage_image)
    if last_result == None:
        print("pass")
    else:
        print("Fail")
else:
    print("fail")