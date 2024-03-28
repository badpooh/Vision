import cv2
import easyocr
import re
import os

from regex import P

class ImgOCR:
    
    def __init__(self, loaded_image_path=None):
        self.loaded_image_path = loaded_image_path
    
    def img_ocr(self, loaded_image_path):
         
        png_files = [os.path.join(loaded_image_path, f) for f in os.listdir(loaded_image_path) if f.endswith('.png')]
        
        for png_file in png_files:
            self.image = cv2.imread(png_file)

        height, width = self.image.shape[:2]

        resized_image_1 = self.image[int(height*0.35):height, int(width*0.185):width]
        resized_image = cv2.resize(resized_image_1, None, None, 2, 2, cv2.INTER_CUBIC)

        reader = easyocr.Reader(['en'], gpu=True)
        results = reader.readtext(resized_image, detail=0)
        #detail=0은 텍스트만 반환
        # results = reader.readtext(resized_image, detail=0)
        # for result in results:
        #     bbox, text, prob = result
        #     top_left = tuple(map(int, bbox[0]))
        #     bottom_right = tuple(map(int, bbox[2]))

        #     # 이미지에 바운딩 박스 그리기
        #     cv2.rectangle(resized_image, top_left, bottom_right, (0, 255, 0), 2)

        #     # 이미지에 텍스트 쓰기 (선택적)
        #     cv2.putText(resized_image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
            
        cv2.imshow('test', resized_image)   
            # 결과 이미지 표시
        # result_str = "\n".join(result)
        # self.main_window.update_text(
        #         "Recognized Numbers:\n" + result_str)
        # print(results)
        
        # 전류 쪽 % 와 A 사이 값 판독
        pattern_number = re.compile(r'\d+(\.\d+)?')  # 숫자 패턴
        # pattern_letter = re.compile(r'[A-Za-z]')     # 문자 패턴

        # 추출된 쌍을 저장할 리스트
        matched_pairs = []

        # # result 리스트를 순회하며 숫자와 문자의 쌍을 찾음
        # for i in range(len(result) - 1):
        #     if pattern_number.match(result[i]) and pattern_letter.match(result[i + 1]):
        #         matched_pair = result[i] + ' ' + result[i + 1]
        #         matched_pairs.append(matched_pair)
        
        # result 리스트를 순회하며 숫자 쌍을 찾음
        for i in range(len(results) - 1):
            if pattern_number.match(results[i]):
                matched_pair = results[i]
                matched_pairs.append(matched_pair)
                
        print(matched_pairs)

        # print(matched_pairs)
        return matched_pairs