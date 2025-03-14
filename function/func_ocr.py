import numpy as np
import cv2
from paddleocr import PaddleOCR
from itertools import chain

from config.config_roi import Configs

class OCRManager:

    def __init__(self, n=3):
        self.n = n
        self.config = Configs(n=self.n)
        self.rois = self.config.roi_params()
        self.phasor_condition = 0

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

    def update_phasor_condition(self, new_c):
        self.phasor_condition = new_c

    def ocr_basic(self, image, roi_keys, test_type):
        image = cv2.imread(image)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {image}")
            return []

        ocr = PaddleOCR(use_gpu=False, use_angle_cls=False, lang='en', use_space_char=True, show_log=False)

        ocr_results = {}
        for roi_key in roi_keys:
            # 이미지 처리
            if self.phasor_condition == 0 and test_type == 0:
                self.update_n(3)
                resized_image = cv2.resize(image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 10, 30, 9, 21)
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                sharpened_image = cv2.filter2D(denoised_image, -1, kernel)
            
            elif self.phasor_condition == 1 and test_type == 0:
                self.update_n(3)
                sharpened_image = cv2.resize(image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
            
            elif test_type == 1:
                self.update_n(2)
                resized_image = cv2.resize(image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 10, 30, 9, 21)
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                sharpened_image = cv2.filter2D(denoised_image, -1, kernel)

            else:
                print(f"Error {self.phasor_condition}")

            if roi_key in self.rois:
                extracted_texts = []
                low_confidence_texts = []
                x, y, w, h = self.rois[roi_key]
                roi_image = sharpened_image[y:y+h, x:x+w]

                # cv2.imshow("test", roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                text_results = ocr.ocr(roi_image, cls=False)
                original_results = []
                
                # text_results를 평탄화
                if text_results:
                    text_results_filtered = [tr for tr in text_results if tr is not None]
                    if text_results_filtered:
                        flat_text_results = list(chain.from_iterable(text_results_filtered))
                        for result in flat_text_results:
                            coords, (text, confidence) = result
                            text = text.strip()
                            confidence = float(confidence)
                            original_results.append((coords, text, confidence))
                            # 신뢰도 검사
                            if confidence >= 0.97:
                                pass
                                # extracted_texts.append(text)
                            else:
                                low_confidence_texts.append((coords, text, confidence))
                    else:
                        flat_text_results = []
                        extracted_texts.append("empty")
                else:
                    print("text_results error")

                height, width = roi_image.shape[:2]
                margin = 5
                # 신뢰도 낮은 텍스트 처리
                for coords, text, conf in low_confidence_texts:
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
                        ### 일반 텍스트 영역 / 97% 초과가 되지않으면 바로 실행
                        if retry_count == 0 and self.phasor_condition == 0:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)
                        
                        ### 그림 영역 / 97% 초과가 되지않으면 바로 실행 (Phasor와 같은 A, B, C 주위에 색박스로 된 부분)
                        elif retry_count == 0 and self.phasor_condition == 1:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, sharpening_kernel)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 100, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            edges = cv2.Canny(thresh_char, 50, 150)
                            char_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                        
                        ### 일반 텍스트 영역 재시도 2번째
                        elif retry_count == 1 and self.phasor_condition == 0:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 150, 255, cv2.THRESH_BINARY)
                            clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(9, 9))
                            enhanced_char = clahe.apply(thresh_char)
                            char_image = cv2.cvtColor(enhanced_char, cv2.COLOR_GRAY2BGR)

                        ### 그림 영역 재시도 2번째
                        elif retry_count == 1 and self.phasor_condition == 1:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)

                        ### 일반 텍스트 영역 재시도 3번째
                        elif retry_count > 1 and self.phasor_condition == 0:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_LANCZOS4)
                            char_image = cv2.Canny(char_image, 0, 200)
                            kernel = np.array([
                                                [-1, -1, -1, -1, -1],
                                                [-1,  1,  1,  1, -1],
                                                [-1,  1,  5,  1, -1],
                                                [-1,  1,  1,  1, -1],
                                                [-1, -1, -1, -1, -1]], dtype=np.float32)
                            char_image = cv2.filter2D(char_image, -1, kernel)

                        elif retry_count > 1 and self.phasor_condition == 1:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)

                        # cv2.imshow("test2", char_image)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()

                        retry_result = ocr.ocr(char_image, cls=False)
                        print(f"재시도 OCR 결과 (시도 {retry_count}):", retry_result)
                        if retry_result and retry_result[0]:
                            flat_retry_result = list(chain.from_iterable(retry_result))
                            for res in flat_retry_result:
                                new_coords, (new_text, new_confidence) = res
                                new_text = new_text.strip()
                                new_confidence = float(new_confidence)

                                if new_confidence >= 0.94 or new_text.lower() == "c" or ((new_text.upper() == "V0" or new_text.upper() == "U0") and new_confidence >= 0.85):
                                    # original_results에서 해당 좌표를 찾아 업데이트
                                    for i, (orig_coords, orig_text, orig_conf) in enumerate(original_results):
                                        if orig_coords == coords:
                                            combined_text = self.merge_texts(orig_text, new_text, orig_coords, new_coords)
                                            original_results[i] = (orig_coords, combined_text, new_confidence)
                                            success = True
                                            break
                                    success = True
                                    break
                        else:
                            print("재시도 후에도 텍스트를 인식하지 못했습니다.")
                        retry_count += 1
                
                extracted_texts = [text for coords, text, conf in original_results]
                extracted_texts = ' '.join(extracted_texts)
                extracted_texts = self.handle_special_cases(extracted_texts)
                if extracted_texts:
                    ocr_results[roi_key] = extracted_texts
            else:
                print(f"{roi_key}가 self.rois에 존재하지 않습니다.")

        for roi_key, text in ocr_results.items():
            print(f'{roi_key}: {text}')

        # 유효한 텍스트만 리스트로 반환
        ocr_results_list = [text for text in ocr_results.values() if text]
        return ocr_results_list

    def merge_texts(self, orig_text, new_text, orig_coords, new_coords):
        if len(new_text) < len(orig_text):
            if new_coords[0][0] > orig_coords[0][0]:
                return orig_text[:len(orig_text)-len(new_text)] + new_text
            else:    
                return new_text + orig_text[len(new_text):]
        else:
            return new_text

    def handle_special_cases(self, text):
        words = text.strip().split()
        processed_words = []
        for i, word in enumerate(words):
            if word == 'V':
                has_word_before = (i > 0)
                has_word_after = (i < len(words) - 1)
                if has_word_before and has_word_after:
                    # 앞뒤로 단어가 있는 경우 'V'를 제외
                    print(f"예외 처리: '{word}'를 결과에서 제외")
                    continue  # 'V'를 결과에서 제외하고 다음 단어로 이동
            processed_words.append(word)
        return ' '.join(processed_words)