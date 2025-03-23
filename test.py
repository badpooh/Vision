from function.func_ocr import PaddleOCRManager
from config.config_roi import ConfigROI as cfr

paddleocr_func = PaddleOCRManager()

class test:
    

    def test001(self):
        image_path = r"C:\rootech\AutoProgram\Vision\results\2025-03-21_16-38-54\2025-03-21_16_52_50_M_S_ME_Voltage.png"
        roi_keys = [cfr.s_vt_primary_ll_vol_1, cfr.s_vt_primary_ll_vol_2]
        setup = 1
        ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys, test_type=setup)

        print(ocr_results)

if __name__ == "__main__":
    start = test()
    start.test001()