import cv2
import easyocr
import numpy as np

image_path = r"C:\Users\Jin\Desktop\Company\Rootech\PNT\old\PyOpenCv\testImage\A2500_1.png"
# 이미지 불러오기

image = cv2.imread(image_path)  # 'image_path.jpg'를 불러올 이미지 파일 경로로 변경하세요.

# 이미지의 너비와 높이 가져오기
height, width  = image.shape[:2]
resized_image_1 = image[int(height*0.229):height, 0:int(width*0.1875)]
resized_image = cv2.resize(resized_image_1, None, None, 2, 2, cv2.INTER_CUBIC)

resized_image_2 = image[int(height*0.26):int(height*0.354), int(width*0.2):width]
resized_image_2_1 = cv2.resize(resized_image_2, None, None, 2, 2, cv2.INTER_CUBIC)

resized_image_3 = image[int(height*0.375):height, int(width*0.212):int(width*0.437)]
resized_image_3_1 = cv2.resize(resized_image_3, None, None, 2, 2, cv2.INTER_CUBIC)

blurred = cv2.GaussianBlur(resized_image, (0, 0), 3)
sharpened = cv2.addWeighted(resized_image, 1.5, blurred, -0.5, 0)

blurred1 = cv2.GaussianBlur(resized_image_2_1, (0, 0), 3)
sharpened1 = cv2.addWeighted(resized_image_2_1, 1.5, blurred1, -0.5, 0)

blurred2 = cv2.GaussianBlur(resized_image_3_1, (0, 0), 3)
sharpened2 = cv2.addWeighted(resized_image_3_1, 1.5, blurred2, -0.5, 0)

reader = easyocr.Reader(['en'], gpu=True)
results = reader.readtext(sharpened, detail=0)
print(results)

results1 = reader.readtext(sharpened1, detail=0)
print(results1)

results2 = reader.readtext(sharpened2, detail=0)
print(results2)

right_text = ["Line-to-Line", "Line-to-Neutral", "LL Fund.", "LN Fund.", "LL THD %", "LN THD %", "Frequency", "Residual"]
right_text1 = ["Line-to-Line Voltage", "Min", "Max"]
right_text2 = ["AB", "BC", "CA", "Average"]

right_text_set = set(text.strip() for text in right_text)
right_text_set1 = set(text.strip() for text in right_text1)
right_text_set2 = set(text.strip() for text in right_text2)

# OCR 결과도 집합으로 변환
ocr_results_set = set(result.strip() for result in results)
ocr_results_set1 = set(result.strip() for result in results1)
ocr_results_set2 = set(result.strip() for result in results2)

# OCR 결과 중에서 정답과 매칭되지 않는 단어 찾기
not_matched_from_ocr = ocr_results_set - right_text_set
not_matched_from_ocr1 = ocr_results_set1 - right_text_set1
not_matched_from_ocr2 = ocr_results_set2 - right_text_set2

# 정답 중에서 OCR 결과와 매칭되지 않는 단어 찾기
not_matched_from_right_text = right_text_set - ocr_results_set
not_matched_from_right_text1 = right_text_set1 - ocr_results_set1
not_matched_from_right_text2 = right_text_set2 - ocr_results_set2

# 매칭되지 않는 단어 프린트
print("OCR에서 읽고 정답과 매칭되지 않는 단어들:")
for word in not_matched_from_ocr:
    print(word)

print("정답에만 있고 OCR에서 매칭되지 않는 단어들:")
for word in not_matched_from_right_text:
    print(word)

# 모두 매칭되는 경우 확인
if not not_matched_from_ocr and not not_matched_from_right_text:
    print("모든 텍스트가 정확히 매칭되었습니다.")
else:
    print("일부 텍스트가 매칭되지 않았습니다.")
    
#####################
print("OCR에서 읽고 정답과 매칭되지 않는 단어들:")
for word in not_matched_from_ocr1:
    print(word)

print("정답에만 있고 OCR에서 매칭되지 않는 단어들:")
for word in not_matched_from_right_text1:
    print(word)

# 모두 매칭되는 경우 확인
if not not_matched_from_ocr1 and not not_matched_from_right_text1:
    print("모든 텍스트가 정확히 매칭되었습니다.")
else:
    print("일부 텍스트가 매칭되지 않았습니다.")

#####################
print("OCR에서 읽고 정답과 매칭되지 않는 단어들:")
for word in not_matched_from_ocr2:
    print(word)

print("정답에만 있고 OCR에서 매칭되지 않는 단어들:")
for word in not_matched_from_right_text2:
    print(word)

# 모두 매칭되는 경우 확인
if not not_matched_from_ocr1 and not not_matched_from_right_text2:
    print("모든 텍스트가 정확히 매칭되었습니다.")
else:
    print("일부 텍스트가 매칭되지 않았습니다.")


# 이미지 보여주기
cv2.imshow('Image with Size Info', sharpened2)
cv2.waitKey(0)
cv2.destroyAllWindows()


# 색 감 비교 코드
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# x, y, w, h = 120, 130, 10, 10 
# selected_area = image_rgb[y:y+h, x:x+w]
# average_color = np.mean(selected_area, axis=(0, 1))
# target_color = np.array([255, 255, 255])
# color_difference = np.linalg.norm(average_color - target_color)

# print("Average color of selected area:", average_color)
# print("Difference from target color:", color_difference)