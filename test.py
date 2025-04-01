from function.func_ocr import PaddleOCRManager
from config.config_roi import ConfigROI as ConfigROI

paddleocr_func = PaddleOCRManager()

class test:
    
    def test001(self):
        image_path = r"C:\rootech\AutoProgram\Vision\image_test\10.10.26.159_2024-08-13_17_28_35_M_H_AN_Curr_Symm.png"
        roi_keys = [ConfigROI.curr_per_a, ConfigROI.curr_per_b]
        setup = 1
        ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys, test_type=setup)

        print(ocr_results)

if __name__ == "__main__":
    start = test()
    start.test001()