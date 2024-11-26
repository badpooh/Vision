from PySide6.QtGui import QIcon, QCursor, QTextCursor
from PySide6.QtCore import QSize, Qt, QTimer, QObject, Signal, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QMenu, QMessageBox, QHeaderView, QTableWidgetItem
from resources_rc import *
import sys
import threading
import os
from datetime import datetime

from ui_dashboard import Ui_MainWindow
from modules.ocr_setting import OcrSetting
from modules.ocr_process import ImgOCR
from demo_test.demo_process import DemoProcess
from demo_test.demo_process import DemoTest
from demo_test.demo_function import ModbusManager, ModbusLabels, TouchManager, Evaluation
from setup_test.setup_setting import SettingWindow
from frame_test.webcam_function import WebCam

class MyDashBoard(QMainWindow, Ui_MainWindow):

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
        self.set_windows = {}
        self.label_load_text = "OCR NO"
        self.label_judge_text = ""
        self.checkbox_states = {
            "voltage": False,
            "current": False,
            "power": False,
            "analysis": False,
            "demand": False,
            }
        self.thread = False
        self.stop_thread = False
        self.ocr = ImgOCR()
        self.modbus_manager = ModbusManager()
        self.meter_setup_process = DemoProcess()
        self.modbus_labels = ModbusLabels()
        self.touch_manager = TouchManager()
        self.evaluation = Evaluation()
        self.alarm = Alarm()
        self.stop_event = threading.Event()
        self.meter_demo_test = DemoTest(self.stop_event)
        self.setting_window = SettingWindow()
        
        self.tableWidget.setHorizontalHeaderLabels(["TITLE", "CONTENT", "RESULT"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(2, 250)

        self.btn_home_1.clicked.connect(self.switch_to_homePage)
        self.btn_home_2.clicked.connect(self.switch_to_homePage)
        self.btn_ui_test_1.clicked.connect(self.switch_to_uiTestPage)
        self.btn_ui_test_2.clicked.connect(self.switch_to_uiTestPage)
        self.btn_setup_test_1.clicked.connect(self.switch_to_setupTestPage)
        self.btn_demo_test.clicked.connect(self.switch_to_setupTestPage)
        self.btn_frame_test_1.clicked.connect(self.switch_to_frameTestPage)
        self.btn_frame_test_2.clicked.connect(self.switch_to_frameTestPage)
        self.btn_connect.clicked.connect(self.setup_connect)
        self.btn_disconnect.clicked.connect(self.setup_disconnect)
        self.btn_select_webcam.clicked.connect(self.select_webcam)
        self.btn_start_webcam.clicked.connect(self.start_webcam)
        self.btn_stop_webcam.clicked.connect(self.stop_webcam)
        self.lineEdit.returnPressed.connect(self.set_focus)
        self.btn_demo_mode_ui_test.clicked.connect(self.demo_ui_test_start)
        self.btn_demo_mode_ui_test_2.clicked.connect(self.demo_ui_test_stop)
        self.btn_demo_mode_ui_test_3.clicked.connect(self.none_ui_test_start)
        self.btn_demo_mode_ui_test_4.clicked.connect(self.none_ui_test_stop)
        self.pushButton_2.clicked.connect(self.ocr_start)
        self.debug_button.clicked.connect(self.debug_test)
        # self.input_ip.returnPressed.connect(self.input_ip_return_pressed)

        self.checkBox_voltage.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "voltage"))
        self.checkBox_current.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "current"))
        self.checkBox_power.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "power"))
        self.checkBox_analysis.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "analysis"))
        self.checkBox_demand.stateChanged.connect(lambda state: self.on_checkbox_changed(state, "demand"))


        self.btn_add_tc.clicked.connect(self.add_box_tc)
        self.tableWidget.cellDoubleClicked.connect(self.on_cell_double_click)
        
        # self.original_stdout = sys.stdout
        # self.original_stderr = sys.stderr
        # sys.stdout = EmittingStream()
        # sys.stdout.text_written.connect(self.write_log)
        # sys.stderr = EmittingStream()
        # sys.stderr.text_written.connect(self.write_log)
        
    # def input_ip_return_pressed(self):
    #     self.device_ip_address = self.input_ip.text()
    #     self.modbus_manager.set_server_ip(self.device_ip_address)
    #     self.modbus_labels.update_clients()
    #     self.input_ip.setStyleSheet("background-color: lightgray;")
    #     QTimer.singleShot(2000, lambda: self.input_ip.setStyleSheet("background-color: white;"))

    # @Slot(str)
    # def write_log(self, text):
    #     self.log.moveCursor(QTextCursor.End)
    #     self.log.insertPlainText(text)
    #     self.log.moveCursor(QTextCursor.End)

    # def closeEvent(self, event):
    #     # 프로그램 종료 시 stdout과 stderr 복원
    #     sys.stdout = self.original_stdout
    #     sys.stderr = self.original_stderr
    #     event.accept()            

    def on_checkbox_changed(self, state, key):
        self.checkbox_states[key] = state == 2  # 2는 체크됨, 0은 체크되지 않음
        print(f"{key.capitalize()} checkbox {'checked' if state == 2 else 'unchecked'}")

    def on_current_checkbox_changed(self, state):
        if state == 2:
            self.current_checked = True
            print("Voltage checkbox checked")
        elif state == 0:
            self.current_checked = False
            print("Voltage checkbox unchecked")
        else:
            print(f"Unknown state: {state}")

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
        self.modbus_manager.tcp_disconnect()

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
        self.meter_setup_process.static_text_measurement()

    def stop_callback(self):
        return self.stop_thread
    
    def on_cell_double_click(self, row, col):
        if col == 0 or col == 1:
            if row not in self.set_windows:
                self.set_windows[row] = self.setting_window.open_new_window(row+1)
            self.set_windows[row].show()

    def demo_ui_test_start(self):
        # if self.modbus_manager.is_connected == True:
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.demo_ui_test, daemon=True)
        self.thread.start()
        # else:
        #     self.alarm.show_connection_error()
            
    def demo_ui_test_stop(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()

    def demo_ui_test(self):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_save_path = os.path.expanduser(f"./results/{current_time}/")
        os.makedirs(base_save_path, exist_ok=True)
        test_mode = "Demo"
        self.meter_demo_test.demo_test_start()
        if self.checkbox_states["voltage"]:
            self.meter_demo_test.demo_test_voltage(base_save_path, test_mode)
            print("Voltage_DemoTest_Done")
        if self.checkbox_states["current"]:
            self.meter_demo_test.demo_test_current(base_save_path, test_mode)
            print("Current_DemoTest_Done")
        if self.checkbox_states["power"]:
            self.meter_demo_test.demo_test_power(base_save_path, test_mode)
            print("Power_DemoTest_Done")
        if self.checkbox_states["analysis"]:
            self.meter_demo_test.demo_test_analysis(base_save_path, test_mode)
            print("Analysis_DemoTest_Done")
        if self.checkbox_states["demand"]:
            self.meter_demo_test.demo_test_demand(base_save_path, test_mode)
            print("Demand_DemoTest_Done")
        else:
            print("Done or Nothing to execute")
        total_csv_files, fail_count = self.evaluation.count_csv_and_failures(base_save_path)
        self.score.setText(f"{fail_count}/{total_csv_files}")

    def none_ui_test_start(self):
        # if self.modbus_manager.is_connected == True:
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.none_ui_test, daemon=True)
        print("None UI TEST Start")
        self.thread.start()
        # else:
        #     self.alarm.show_connection_error()
            
    def none_ui_test_stop(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()

    def none_ui_test(self):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_save_path = os.path.expanduser(f"./results/{current_time}/")
        os.makedirs(base_save_path, exist_ok=True)
        test_mode = "None"
        self.touch_manager.uitest_mode_start()
        if self.checkbox_states["voltage"]:
            self.meter_demo_test.demo_test_voltage(base_save_path, test_mode)
            print("Voltage_DemoTest_Done")
        if self.checkbox_states["current"]:
            self.meter_demo_test.demo_test_current(base_save_path, test_mode)
            print("Current_DemoTest_Done")
        if self.checkbox_states["power"]:
            self.meter_demo_test.demo_test_power(base_save_path, test_mode)
            print("Power_DemoTest_Done")
        if self.checkbox_states["analysis"]:
            self.meter_demo_test.demo_test_analysis(base_save_path, test_mode)
            print("Analysis_DemoTest_Done")
        if self.checkbox_states["demand"]:
            self.meter_demo_test.demo_test_demand(base_save_path, test_mode)
            print("Demand_DemoTest_Done")
        else:
            print("Done or Nothing to execute")
        total_csv_files, fail_count = self.evaluation.count_csv_and_failures(base_save_path)
        self.score.setText(f"{fail_count}/{total_csv_files}")

    def debug_test(self):
        self.meter_demo_test.testcode01()

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
        label_text = ", ".join(
            checkBox_contents) if checkBox_contents else "데이터 없음"

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
                label_load.setText(
                    "OCR OK" if self.images_loaded else "OCR NO")
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

    def add_box_tc(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        for col in range(3):
            readonly_item = QTableWidgetItem()
            readonly_item.setFlags(readonly_item.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, col, readonly_item)

    def create_menu(self, tc_box_index):
        menu = QMenu()
        actionCMC = menu.addAction("CMC")
        actionOCR = menu.addAction("OCR")

        actionCMC.triggered.connect(self.actionCMC_clicked)
        actionOCR.triggered.connect(
            lambda: self.open_ocr_setting(tc_box_index))

        # 메뉴를 보이게 함
        menu.exec_(QCursor.pos())

    def actionCMC_clicked(self):
        print("CMC clicked")

    def open_ocr_setting(self, tc_box_index):
        ocr_setting = OcrSetting(
            tc_box_index, callback=self.callback_ocr_list, load_callback=self.callback_ocr_load)
        ocr_setting.show()
        self.ocr_settings[tc_box_index] = ocr_setting
        
class Alarm:
    
    def show_connection_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Connection Error")
        msg.setText("장치와 미연결 상태")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
class EmittingStream(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass  # 필요한 경우 구현