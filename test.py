from paddleocr import PaddleOCR
import cv2

ocr = PaddleOCR(
    use_angle_cls=False,
    lang='en',
    use_space_char=True,
    show_log=True,
    use_gpu=False,
    device='GPU',
    use_openvino=True
)

image_path = r"C:\PNT\09.AutoProgram\AutoProgram\image_test\vol_pow\10.10.26.156_2024-08-09_09_48_40_M_H_CU_RMS.png"
image = cv2.imread(image_path)
result = ocr.ocr(image, cls=False)
print(result)