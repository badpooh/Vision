from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog)
from PySide6.QtCore import Signal, QObject
import os, glob
from .ui_ocr_setting import Ui_OCR_SETTING

class OcrSetting(QWidget, Ui_OCR_SETTING):
    def __init__(self, tc_box_index, callback=None, load_callback=None):
        super().__init__()  # 인덱스를 내부 상태로 저장
        self.setupUi(self)
        self.btn_save.clicked.connect(self.save_setting)
        self.btn_load.clicked.connect(self.load_photo)
        self.tc_box_index = tc_box_index
        self.callback = callback
        self.checkBox_contents = []
        self.load_callback = load_callback
        self.image_files = []
    
    def update_check_box_contents(self):
        self.checkBox_contents = []
        if self.check_box_1.isChecked():
            self.checkBox_contents.append("VOLTAGE L-L")
        if self.check_box_2.isChecked():
            self.checkBox_contents.append("VOLTAGE L-N")
        if self.check_box_3.isChecked():
            self.checkBox_contents.append("CURRENT RMS")
    
    def save_setting(self):
        self.update_check_box_contents()
        if self.callback:
            # 저장 시 콜백 함수에 인덱스와 체크박스 내용을 전달
            self.callback(self.tc_box_index, self.checkBox_contents)

    def load_photo(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        # image_files = glob.glob(os.path.join(folder_path, '*.png')) + glob.glob(os.path.join(folder_path, '*.jpeg')) + glob.glob(os.path.join(folder_path, '*.jpg'))
        if folder_path and self.load_callback:
                self.load_callback(self.tc_box_index, folder_path)
                
        else:
            print("no files")