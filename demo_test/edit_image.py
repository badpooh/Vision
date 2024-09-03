import cv2
import easyocr
from roi_and_answer import RoiAnswer

voltage_image_path = r".\image_test\a7300_mea_voltage.png"

roi_and_answer = RoiAnswer()
rois = roi_and_answer.roi()

class EditImage:

    ########################## 이미지 커팅 기본 method ##########################
    def image_cut(self, image, height_ratio_start, height_ratio_end, width_ratio_start, width_ratio_end):
        height, width = image.shape[:2]
        cropped_image = image[int(height*height_ratio_start):int(height*height_ratio_end),
                            int(width*width_ratio_start):int(width*width_ratio_end)]
        resized_image = cv2.resize(cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # 이미지 블러 처리 및 선명하게 만들기
        blurred_image = cv2.GaussianBlur(resized_image, (0, 0), 3)
        sharpened_image = cv2.addWeighted(resized_image, 1.5, blurred_image, -0.5, 0)
        return sharpened_image
    ####################################################
    
    def image_cut_custom(self, image):
        image = cv2.imread(image)
        resized_image = cv2.resize(image, None, None, 3, 3, cv2.INTER_CUBIC)
        blurred_image = cv2.GaussianBlur(resized_image, (0, 0), 3)
        sharpened_image = cv2.addWeighted(resized_image, 1.5, blurred_image, -0.5, 0)

        reader = easyocr.Reader(['en'])

        # 각 ROI에 대해 OCR 처리 및 결과 수집
        ocr_results = {}
        for roi_key, (x, y, w, h) in rois.items():
            roi_image = sharpened_image[y:y+h, x:x+w]
            cv2.imshow('Image with Size Info', roi_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            text_results = reader.readtext(roi_image, paragraph=False)  # 해당 ROI에 대해 OCR 수행

            # 추출된 텍스트 합치기
            extracted_texts = ' '.join([text[1] for text in text_results])

            ocr_results[roi_key] = extracted_texts

        # OCR 결과 출력
        for roi_key, text in ocr_results.items():
            print(f'ROI {roi_key}: {text}')

    
ed = EditImage()
ed.image_cut_custom(voltage_image_path)   