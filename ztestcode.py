import cv2
import numpy as np
from paddleocr import PaddleOCR
from itertools import chain

from demo_test.demo_config import ConfigSetup
from demo_test.demo_config import ConfigROI as ecroi

class OCRManager:

    def __init__(self, n=3):
        self.n = n
        self.config = ConfigSetup(n=self.n)
        self.rois = self.config.roi_params()

    def color_detection(self, image, color_data):
        x, y, w, h, R, G, B = color_data
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        selected_area = image_rgb[y:y+h, x:x+w]
        average_color = np.mean(selected_area, axis=(0, 1))
        target_color = np.array([R, G, B])
        color_difference = np.linalg.norm(average_color - target_color)
        return color_difference
    
    def update_n(self, new_n):
        self.n = new_n
        self.config.update_n(new_n)
        self.rois = self.config.roi_params()
        # print(f"n 값이 {new_n}으로 변경되었습니다.")

    def ocr_basic(self, image, roi_keys):
        image = cv2.imread(image)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {image}")
            return []

        ocr = PaddleOCR(use_angle_cls=False, lang='en', use_space_char=True, show_log=False)

        ocr_results = {}
        for roi_key in roi_keys:
             # 이미지 처리
            self.update_n(3)
            resized_image = cv2.resize(image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
            gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 10, 30, 9, 21)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # 샤프닝 커널
            sharpened_image = cv2.filter2D(denoised_image, -1, kernel)

            if roi_key in self.rois:
                x, y, w, h = self.rois[roi_key]
                roi_image = sharpened_image[y:y+h, x:x+w]

                # cv2.imshow("test", roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

                # OCR 처리
                text_results = ocr.ocr(roi_image, cls=False)
                
                # text_results를 평탄화
                if text_results:
                    flat_text_results = list(chain.from_iterable(text_results))
                else:
                    flat_text_results = []

                extracted_texts = []
                low_confidence_texts = []
                for result in flat_text_results:
                    coords, (text, confidence) = result
                    text = text.strip()
                    confidence = float(confidence)

                    # 신뢰도 검사
                    if confidence >= 0.98:
                        extracted_texts.append(text)
                    else:
                        low_confidence_texts.append((text, confidence, coords))

                height, width = roi_image.shape[:2]
                margin = 5
                # 신뢰도 낮은 텍스트 처리
                for text, conf, coords in low_confidence_texts:
                    max_retries = 3
                    retry_count = 0
                    success = False

                    print(f"ROI '{roi_key}'에서 신뢰도 98% 미만의 텍스트:")
                    print(f" - '{text}' (신뢰도: {conf * 100:.2f}%)")
                    # coords를 사용하여 해당 텍스트 영역 이미지 추출
                    x_min = max(0, int(min([pt[0] for pt in coords])) - margin)
                    x_max = min(width, int(max([pt[0] for pt in coords])) + margin)
                    y_min = max(0, int(min([pt[1] for pt in coords])) - margin)
                    y_max = min(height, int(max([pt[1] for pt in coords])) + margin)
                    text_roi = roi_image[y_min:y_max, x_min:x_max]

                    # 이미지 전처리 및 OCR 재시도
                    if text_roi.size == 0:
                        continue  # 유효하지 않은 영역은 건너뜁니다

                    
                    while retry_count < max_retries and not success:
                        char_image = text_roi.copy()
                        if retry_count == 1:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # 샤프닝 커널
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)
                        
                        elif retry_count > 1:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # 샤프닝 커널
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)
                            
                            cv2.imshow("test2", char_image)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()

                        

                        retry_result = ocr.ocr(char_image, cls=False)
                        print(f"재시도 OCR 결과 (시도 {retry_count}):", retry_result)
                        if retry_result and retry_result[0]:
                            # 결과에서 텍스트와 신뢰도 추출
                            try:
                                new_text_info = retry_result[0][1]
                                new_text = new_text_info[0].strip()
                                new_confidence = float(new_text_info[1])
                            except:
                                # 결과 구조가 다를 경우
                                new_text_info = retry_result[0][0][1]
                                new_text = new_text_info[0].strip()
                                new_confidence = float(new_text_info[1])

                            if new_confidence >= 0.95 or new_text == "c" or new_text == "C":
                                extracted_texts.append(new_text)
                                success = True  # 성공적으로 인식하면 반복 종료
                            else:
                                print(f"재시도 후에도 신뢰도 낮음: '{new_text}' (신뢰도: {new_confidence * 100:.2f}%)")
                        else:
                            print("재시도 후에도 텍스트를 인식하지 못했습니다.")
                        retry_count += 1  # 재시도 횟수 증가

                extracted_texts = ' '.join(extracted_texts)
                # extracted_texts = self.handle_special_cases(extracted_texts)
                if extracted_texts:
                    ocr_results[roi_key] = extracted_texts
            else:
                print(f"{roi_key}가 self.rois에 존재하지 않습니다.")

        for roi_key, text in ocr_results.items():
            print(f'{roi_key}: {text}')

        # 유효한 텍스트만 리스트로 반환
        ocr_results_list = [text for text in ocr_results.values() if text]
        return ocr_results_list

# 테스트 코드
if __name__ == "__main__":
    ocr_manager = OCRManager()

    image_path = r"C:\PNT\09.AutoProgram\AutoProgram\image_test\10.10.26.159_2024-11-25_15_34_17_M_H_VO_RMS.png"

    roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]

    results = ocr_manager.ocr_basic(image_path, roi_keys_meas)
    print(f"OCR 결과: {results}")
