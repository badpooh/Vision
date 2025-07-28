import numpy as np
import cv2
from paddleocr import PaddleOCR
# from itertools import chain # 더 이상 필요하지 않으므로 주석 처리하거나 삭제
import os

from config.config_roi import Configs

class PaddleOCRManager:

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

    def paddleocr_basic(self, image, roi_keys, test_type):
        try:
            current_script_path = os.path.abspath(__file__)
        except NameError:
            current_script_path = os.path.abspath('.')

        script_directory = os.path.dirname(current_script_path)

        rec_model_folder_path = os.path.join(script_directory, '..', 'rec') # 현재 이 부분은 사용되지 않는 것 같습니다.
        rec_model_folder_path = os.path.normpath(rec_model_folder_path)
        rec_model_folder_path = rec_model_folder_path.replace('\\', '/')

        image = cv2.imread(image)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {image}")
            return []

        # PaddleOCR 초기화 (모델 지정은 필요시 추가)
        # ocr = PaddleOCR(use_gpu=True, use_angle_cls=False, lang='en', use_space_char=True, show_log=False, rec_model_dir=rec_model_folder_path)

        
        ocr = PaddleOCR(text_detection_model_name="PP-OCRv5_mobile_det",
                        text_recognition_model_name="latin_PP-OCRv5_mobile_rec",
                        use_doc_orientation_classify=False,
                        use_doc_unwarping=False,
                        use_textline_orientation=False)

        # OCR 결과를 저장할 딕셔너리    


        ocr_results = {} # 최종 결과를 저장할 딕셔너리
        for roi_key in roi_keys:
            # 이미지 전처리 로직 (이 부분은 그대로 유지)
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
                self.update_n(1)
                sharpened_image = image

            else:
                print(f"Error {self.phasor_condition}")

            if roi_key in self.rois:
                # 초기화는 루프 내부에서 해당 ROI에만 적용되어야 합니다.
                extracted_texts = []
                low_confidence_texts = []
                original_results = [] # 각 ROI별로 초기화

                x, y, w, h = self.rois[roi_key]
                roi_image = sharpened_image[y:y+h, x:x+w]

                text_results = ocr.ocr(roi_image)
                # print(f"Initial OCR results for ROI '{roi_key}':", text_results) # 디버깅용 출력

                if text_results and len(text_results) > 0:
                    image_result_dict = text_results[0]

                    if 'dt_polys' in image_result_dict and \
                       'rec_texts' in image_result_dict and \
                       'rec_scores' in image_result_dict:

                        dt_polys = image_result_dict['dt_polys']
                        rec_texts = image_result_dict['rec_texts']
                        rec_scores = image_result_dict['rec_scores']

                        # OCR 결과가 없는 경우도 처리 (예: 빈 이미지 ROI)
                        if not dt_polys: # dt_polys가 비어있으면 인식된 텍스트가 없음
                            print(f"ROI '{roi_key}': No text detected.")
                            extracted_texts.append("empty") # 추출된 텍스트가 없음을 표시
                        else:
                            for coords, text, confidence in zip(dt_polys, rec_texts, rec_scores):
                                text = text.strip()
                                confidence = float(confidence)
                                original_results.append((coords, text, confidence))

                                if confidence >= 0.96:
                                    extracted_texts.append(text)
                                else:
                                    low_confidence_texts.append((coords, text, confidence))
                    else:
                        print(f"Warning: Expected keys (dt_polys, rec_texts, rec_scores) not found in OCR result for ROI '{roi_key}'.")
                        extracted_texts.append("empty")
                else:
                    print(f"No OCR results received for ROI '{roi_key}' from ocr.ocr().")
                    extracted_texts.append("empty")

                # 신뢰도 낮은 텍스트 처리 (재시도 로직)
                height, width = roi_image.shape[:2]
                margin = 5
                
                # 'success' 변수를 여기서 초기화하여 각 low_confidence_texts 항목에 대해 독립적으로 처리
                
                for i, (coords, text, conf) in enumerate(low_confidence_texts):
                    max_retries = 3
                    retry_count = 0
                    success = False # 각 저신뢰도 텍스트 항목에 대해 초기화

                    print(f"ROI '{roi_key}'에서 신뢰도 96% 미만의 텍스트 재시도: '{text}' (신뢰도: {conf * 100:.2f}%)")
                    
                    x_min = max(0, int(min([pt[0] for pt in coords])) - margin)
                    x_max = min(width, int(max([pt[0] for pt in coords])) + margin)
                    y_min = max(0, int(min([pt[1] for pt in coords])) - margin)
                    y_max = min(height, int(max([pt[1] for pt in coords])) + margin)
                    text_roi = roi_image[y_min:y_max, x_min:x_max]

                    if text_roi.size == 0:
                        print(f"Skipping empty text_roi for '{text}'.")
                        continue

                    while retry_count < max_retries and not success:
                        char_image = text_roi.copy()
                        
                        # 이미지 전처리 로직 (복잡하므로 조건문은 그대로 유지)
                        if retry_count == 0 and self.phasor_condition == 0 and test_type == 0:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)
                        
                        elif retry_count == 0 and self.phasor_condition == 1 and test_type == 0:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, sharpening_kernel)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 100, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            edges = cv2.Canny(thresh_char, 50, 150)
                            char_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                        
                        elif retry_count == 1 and self.phasor_condition == 0 and test_type == 0:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 150, 255, cv2.THRESH_BINARY)
                            clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(9, 9))
                            enhanced_char = clahe.apply(thresh_char)
                            char_image = cv2.cvtColor(enhanced_char, cv2.COLOR_GRAY2BGR)

                        elif retry_count == 1 and self.phasor_condition == 1 and test_type == 0:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)

                        elif retry_count > 1 and self.phasor_condition == 0 and test_type == 0:
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

                        elif retry_count > 1 and self.phasor_condition == 1 and test_type == 0:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)

                        elif retry_count == 0 and self.phasor_condition == 0 and test_type == 1:
                            self.update_n(1)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                        
                        # --- 여기부터 중요! 재시도 OCR 결과 처리 ---
                        retry_ocr_results = ocr.ocr(char_image) # 변수명 변경 (retry_result -> retry_ocr_results)
                        # print(f"재시도 OCR 결과 (시도 {retry_count}):", retry_ocr_results) # 디버깅용 출력

                        if retry_ocr_results and len(retry_ocr_results) > 0:
                            image_retry_result_dict = retry_ocr_results[0] # 첫 번째 이미지 결과 딕셔너리 추출

                            if 'dt_polys' in image_retry_result_dict and \
                               'rec_texts' in image_retry_result_dict and \
                               'rec_scores' in image_retry_result_dict:

                                dt_polys_retry = image_retry_result_dict['dt_polys']
                                rec_texts_retry = image_retry_result_dict['rec_texts']
                                rec_scores_retry = image_retry_result_dict['rec_scores']

                                # zip()을 사용하여 각 텍스트 라인 정보를 올바르게 언팩
                                for new_coords_retry, new_text_retry, new_confidence_retry in zip(dt_polys_retry, rec_texts_retry, rec_scores_retry):
                                    new_text_retry = new_text_retry.strip()
                                    new_confidence_retry = float(new_confidence_retry)

                                    # 재시도 성공 조건
                                    if new_confidence_retry >= 0.98 or \
                                       new_text_retry.lower() == "c" or \
                                       ((new_text_retry.upper() == "V0" or new_text_retry.upper() == "U0") and new_confidence_retry >= 0.85):

                                        # original_results 리스트에서 해당 원본 텍스트를 찾아 업데이트
                                        # 현재 루프의 'coords' 변수(원본 low_confidence_texts에서 온)와 비교하여 업데이트
                                        for k, (orig_coords, orig_text, orig_conf) in enumerate(original_results):
                                            # 좌표 비교 (Numpy array일 수 있으므로 np.array_equal 사용 권장)
                                            # 또는 리스트로 변환하여 비교: orig_coords.tolist() == coords.tolist()
                                            if np.array_equal(orig_coords, coords): # <-- 여기에서 'coords'는 외부 루프의 저신뢰도 텍스트의 좌표
                                                combined_text = self.merge_texts(orig_text, new_text_retry, orig_coords, new_coords_retry)
                                                original_results[k] = (orig_coords, combined_text, new_confidence_retry)
                                                
                                                # extracted_texts 리스트에도 업데이트된 텍스트 추가 (혹은 해당 항목 교체)
                                                # 이 부분은 현재 로직에 따라 다를 수 있습니다.
                                                # 예를 들어, 해당 텍스트가 원래 extracted_texts에 없었다면 추가, 있었다면 교체
                                                if orig_text in extracted_texts:
                                                    extracted_texts[extracted_texts.index(orig_text)] = combined_text
                                                else:
                                                    extracted_texts.append(combined_text)

                                                success = True # 성공 플래그 설정
                                                break # original_results 업데이트 성공했으니 내부 루프 탈출
                                        
                                        # 재시도 루프 자체를 중단 (하나라도 성공하면 멈춤)
                                        if success:
                                            break # 'for new_coords, new_text, new_confidence' 루프 탈출
                                
                                if success: # 이 조건은 zip 루프를 완전히 빠져나왔을 때 성공 여부 확인
                                    break # while retry_count 루프 탈출 (성공했으니 더 시도할 필요 없음)
                                else:
                                    print(f"조건을 만족하는 재시도 텍스트를 찾지 못했습니다. 재시도 횟수: {retry_count+1}")
                                    retry_count += 1 # 조건 불만족 시 retry_count 증가
                            else:
                                print(f"Warning: Expected keys (dt_polys, rec_texts, rec_scores) not found in retry OCR result for ROI '{roi_key}'.")
                                retry_count += 1 # 결과 딕셔너리에 키가 없으면 다음 재시도로 넘어감
                        else:
                            print(f"No OCR results received from retry ocr.ocr() for ROI '{roi_key}' (Attempt {retry_count+1}).")
                            retry_count += 1 # OCR 결과 자체가 없으면 다음 재시도로 넘어감
                    
                    # 모든 재시도 후에도 성공하지 못했다면
                    if not success:
                        print(f"재시도 후에도 ROI '{roi_key}'의 텍스트 '{text}'에 대해 조건을 만족하는 텍스트를 찾지 못했습니다.")
                        # 필요하다면 original_results 또는 extracted_texts에 해당 텍스트를 어떻게 처리할지 결정
                        # 예: original_results[i] = (coords, orig_text, 0.0) 또는 extracted_texts.append("NOT_RECOGNIZED")

                # 각 ROI 처리 후 ocr_results에 결과 저장 (이전 로직과 동일)
                # 추출된 텍스트가 있다면 첫 번째 텍스트를 저장, 없으면 "empty"
                if extracted_texts:
                    ocr_results[roi_key] = extracted_texts[0] # 첫 번째 텍스트만 저장
                else:
                    ocr_results[roi_key] = "empty" # 텍스트가 없는 경우
            else:
                print(f"ROI '{roi_key}'를 찾을 수 없습니다.")
                ocr_results[roi_key] = "Error: ROI not found"

        # 최종 결과 출력
        for roi_key, text in ocr_results.items():
            print(f'{roi_key}: {text}')

        # 유효한 텍스트만 리스트로 반환
        ocr_results_list = [text for text in ocr_results.values() if text and text != "empty" and "Error" not in text]
        return ocr_results_list

    def merge_texts(self, orig_text, new_text, orig_coords, new_coords):
        if len(new_text) < len(orig_text):
            # 병합 로직 (이전과 동일)
            # 여기서는 orig_coords, new_coords가 array일 수도 있으므로, 필요시 .tolist() 처리
            # np.array_equal 사용 또는 min, max 값으로 대략적인 위치 비교
            if new_coords[0][0] > orig_coords[0][0]: # 첫 번째 X 좌표 비교
                return orig_text[:len(orig_text)-len(new_text)] + new_text
            else:    
                return new_text + orig_text[len(new_text):]
        else:
            return new_text

    def handle_special_cases(self, text):
        if not isinstance(text, str):
            print(f"Warning: handle_special_cases received non-string input: {type(text)}")
            return "handle_special_cases type error"
        words = text.strip().split()
        processed_words = []
        for i, word in enumerate(words):
            original_word = word
            if word == 'V':
                has_word_before = (i > 0)
                has_word_after = (i < len(words) - 1)
                if has_word_before and has_word_after:
                    print(f"예외 처리: '{word}'를 결과에서 제외")
                    continue
            if word.upper() == 'O':
                has_word_before = (i > 0)
                has_word_after = (i < len(words) - 1)
                if not has_word_before or not has_word_after:
                    print(f"예외 처리 (Isolated O->0): '{original_word}'를 '0'으로 변경")
                    word = '0'
            processed_words.append(word)
        return ' '.join(processed_words)