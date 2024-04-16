import cv2
import easyocr
import numpy as np
from itertools import chain
from pymodbus.client import ModbusTcpClient as ModbusClient

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

# 색 감 비교 코드
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# x, y, w, h = 120, 130, 10, 10 
# selected_area = image_rgb[y:y+h, x:x+w]
# average_color = np.mean(selected_area, axis=(0, 1))
# target_color = np.array([255, 255, 255])
# color_difference = np.linalg.norm(average_color - target_color)

# print("Average color of selected area:", average_color)
# print("Difference from target color:", color_difference)



client = ModbusClient('10.10.26.156', port=502)

modbus_mappings = {
6001: {"description": "Wiring", "values": {0: "3P4W", 1: "3P3W"}},
6003: {"description": "Reference voltage", "type": "uint32"},
6005: {"description": "PT Primary Voltage", "type": "uint32"},
6007: {"description": "PT Secondary Voltage", "type": "uint16"},
6008: {"description": "Minimum measured secondary voltage", "type": "uint16"},
6009: {"description": "Reference voltage mode", "values": {0:"Line-to-Line", 1:"Line-to-Neutral"}},
6040: {"description": "Rotating sequence", "values": {0:"Auto", 1:"Positive", 2:"Negative"}},
6051: {"description": "Sliding reference voltage type", "values": {0: "Reference voltage", 1: "Sliding reference voltage"}},
}


def read_modbus_value(client, address):
    """주어진 주소에서 Modbus 값을 읽고, 매핑된 문자열로 변환합니다."""
    response = client.read_holding_registers(address, count=1)
    if response.isError():
        print("Error reading Modbus address", address)
        return None
    else:
        value = response.registers[0]
        return modbus_mappings[address]["values"].get(value, "Unknown Value")

# Modbus 클라이언트 설정 및 데이터 읽기

# client.connect()

# wiring_status = read_modbus_value(client, 6001)
# print("Wiring Configuration:", wiring_status)

# client.close()


def read_uint32(client, address):
    """주어진 주소에서 32비트 데이터를 읽어 반환합니다."""
    response = client.read_holding_registers(address, count=2)  # 2개 레지스터 읽기
    if response.isError():
        print("Error reading Modbus address", address)
        return None
    else:
        # 두 레지스터 결합 (Big Endian)
        high_register = response.registers[0]
        low_register = response.registers[1]
        value = (low_register << 16) + high_register  # 상위 레지스터를 왼쪽으로 16비트 시프트 후 하위 레지스터와 합산
        return value

client.connect()

vt_primary_voltage = read_uint32(client, 6003)  # 32비트 값 읽기 예
print("VT Primary Voltage:", vt_primary_voltage)

client.close()

