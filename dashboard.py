from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMenu, QLabel, QSpacerItem, QSizePolicy
from resources_rc import*

from ui_dashboard import Ui_MainWindow
from modules.ocr_setting import OcrSetting
from modules.ocr_process import ImgOCR
from setup_test.setup_process import SetupProcess
from frame_test.webcam_function import WebCam



class MyDashBoard(QMainWindow, Ui_MainWindow):
    
    ocr = ImgOCR()
    meter_setup_process = SetupProcess()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("My DashBoard")
        self.icon_name_widget.setHidden(True)
        self.stackedWidget.setCurrentIndex(0)
        self.label_name = ""
        self.box_list = [] 
        self.tc_box_index = 0
        self.ocr_settings = {}
        self.label_load_text = "OCR NO"
        self.label_judge_text = ""
        
        self.btn_home_1.clicked.connect(self.switch_to_homePage)
        self.btn_home_2.clicked.connect(self.switch_to_homePage)
        self.btn_ui_test_1.clicked.connect(self.switch_to_uiTestPage)
        self.btn_ui_test_2.clicked.connect(self.switch_to_uiTestPage)
        self.btn_setup_test_1.clicked.connect(self.switch_to_setupTestPage)
        self.btn_setup_test_2.clicked.connect(self.switch_to_setupTestPage)
        self.btn_frame_test_1.clicked.connect(self.switch_to_frameTestPage)
        self.btn_frame_test_2.clicked.connect(self.switch_to_frameTestPage)
        self.btn_connect.clicked.connect(self.setup_connect)
        self.btn_disconnect.clicked.connect(self.setup_disconnect)
        self.btn_setup_test_start.clicked.connect(self.setup_start)
        self.btn_setup_read.clicked.connect(self.setup_read)
        self.btn_select_webcam.clicked.connect(self.select_webcam)
        self.btn_start_webcam.clicked.connect(self.start_webcam)
        self.btn_stop_webcam.clicked.connect(self.stop_webcam)
        self.lineEdit.returnPressed.connect(self.set_focus)
        self.btn_FT_measurement.clicked.connect(self.fixed_text_measurement)
        
        self.pushButton_2.clicked.connect(self.ocr_start)
        
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.scrollAreaLayout)
        
        self.btn_add_tc.clicked.connect(self.add_box_tc)
        
    def switch_to_homePage(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def switch_to_uiTestPage(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def switch_to_setupTestPage(self):
        self.stackedWidget.setCurrentIndex(2)
    
    def switch_to_frameTestPage(self):
        self.stackedWidget.setCurrentIndex(3)
        
    def setup_connect(self):
        self.meter_setup_process.modbus_connect()
        
    def setup_disconnect(self):
        self.meter_setup_process.modbus_discon()

    def setup_start(self):
        self.meter_setup_process.setup_test001()

    def setup_read(self):
        self.meter_setup_process.read_setup_mapping()
        
    def select_webcam(self):
        self.webcam = WebCam()
        
    def start_webcam(self):
        self.webcam.start_streaming()
        
    def stop_webcam(self):
        self.webcam.stop_streaming()
        
    def fixed_text_measurement(self):
        self.meter_setup_process.mea_demo_mode()

    def set_focus(self):
        try:
            focus_value = int(self.lineEdit.text())
            self.webcam.focus_value = focus_value
            self.webcam.adjust_focus()
        except ValueError:
            print("유효한 숫자를 입력하세요.")
        self.lineEdit.clear()
        self.webcam.adjust_focus()
        self.lineEdit.clear()
    
    def callback_ocr_list(self, tc_box_index, checkBox_contents):
        print(f"Box {checkBox_contents} index: {tc_box_index}")
        label_text = ", ".join(checkBox_contents) if checkBox_contents else "데이터 없음"
    
        # box_list에서 올바른 라벨을 찾습니다.
        for _, label, index, _, _ in self.box_list:
            if index == tc_box_index:
                label.setText(label_text)  # QLabel의 setText 메서드 호출
                break
            
    def callback_ocr_load(self, tc_box_index, image_files):
        self.saved_image_files = image_files
        self.images_loaded = bool(self.saved_image_files)
        
        for _, label, index, label_load, _ in self.box_list:
            if index == tc_box_index:
                label_load.setText("OCR OK" if self.images_loaded else "OCR NO")
                break
        
    def ocr_start(self):
        if self.saved_image_files:
            # print(self.saved_image_files)
            self.ocr_results = self.ocr.img_ocr(self.saved_image_files)
        # print(self.ocr_results)
            self.ocr_judge(self.tc_box_index)
    
    def ocr_judge(self, tc_box_index):
        if 510 < float(self.ocr_results[0]) < 520:
            self.judge = True
            print("pass")
        else:
            self.judge = False
            print("fail")
            
        print("box_list:", self.box_list)
        print("tc_box_index:", tc_box_index)
        for _, label, index, _, label_judge in self.box_list:
            print("Looping through box_list:", index)
            if index + 1 == tc_box_index:
                label_judge.setText("PASS" if self.judge else "FAIL")
            print("Found matching index:", label_judge)
            break

    def add_box_tc(self, checkBox_contents=[], images_loaded=False, judge=None):
        if checkBox_contents:
            label_name = ", ".join(checkBox_contents)
        else:
            label_name = ""
        
        new_widget = QWidget()
        new_widget_layout = QHBoxLayout(new_widget)
        new_widget.setLayout(new_widget_layout)
        new_widget.setStyleSheet(u"QWidget{background-color: lightgrey;}" 
                                 "QPushButton {color:black; max-width:25px; max-height:100px;}")
        new_widget.setMinimumHeight(100)
        new_widget.setMaximumHeight(100)
        
        # QLabel 추가
        label_index = QLabel(str(self.tc_box_index))
        label_item = QLabel(str(label_name))
        
        label_load_text = "OCR OK" if images_loaded else "OCR NO"
        label_load = QLabel(label_load_text)
        label_judge_text = "PASS" if judge is True else ("" if judge is None else "FAIL")
        label_judge = QLabel(label_judge_text)
        
        label_item.setAlignment(Qt.AlignCenter)
        new_widget_layout.addWidget(label_index)
        new_widget_layout.addWidget(label_item)
        new_widget_layout.addWidget(label_load)
        new_widget_layout.addWidget(label_judge)
        
        self.spacer = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        new_widget_layout.addItem(self.spacer)
        
        new_widget_setting = QPushButton(new_widget)
        new_widget_setting.setObjectName(u"Setting")
        self.icon = QIcon()
        self.icon.addFile(u":/images/more.png", QSize(), QIcon.Normal, QIcon.Off)
        new_widget_setting.setIcon(self.icon)
        new_widget_layout.addWidget(new_widget_setting)
        current_index = self.tc_box_index
        new_widget_setting.clicked.connect(lambda: self.create_menu(current_index))
        
        # 스크롤 영역에 새로운 위젯 추가
        self.scrollAreaLayout.addWidget(new_widget)
        
        self.box_list.append((new_widget, label_item, self.tc_box_index, label_load, label_judge))
        self.tc_box_index += 1
          
    def create_menu(self, tc_box_index):
        menu = QMenu()
        actionCMC = menu.addAction("CMC")
        actionOCR = menu.addAction("OCR")

        actionCMC.triggered.connect(self.actionCMC_clicked)
        actionOCR.triggered.connect(lambda: self.open_ocr_setting(tc_box_index))

        # 메뉴를 보이게 함
        menu.exec_(QCursor.pos())

    def actionCMC_clicked(self):
        print("CMC clicked")

    def open_ocr_setting(self, tc_box_index):
        ocr_setting = OcrSetting(tc_box_index, callback=self.callback_ocr_list, load_callback=self.callback_ocr_load)
        ocr_setting.show()
        self.ocr_settings[tc_box_index] = ocr_setting
    