from PySide6.QtGui import QIcon, QCursor, QTextCursor
from PySide6.QtCore import QSize, Qt, QObject, Signal, QThread
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QMenu, QMessageBox, QHeaderView, QTableWidgetItem, QFileDialog
from resources_rc import *
import sys
import threading
import os
from datetime import datetime
import time
import xml.etree.ElementTree as ET
from functools import partial

from ui_dashboard import Ui_MainWindow
from modules.ocr_setting import OcrSetting
from modules.ocr_process import ImgOCR
from demo_test.demo_process import DemoProcess
from demo_test.demo_process import DemoTest
from demo_test.demo_function import ModbusManager, ModbusLabels, TouchManager, Evaluation

from setup_test.setup_function import SetupModbusManager
from setup_test.setup_setting import SettingWindow
from setup_test.setup_setting import SettingIP
from setup_test.setup_db import IPDataBase

from frame_test.webcam_function import WebCam

image_directory = r"\\10.10.20.30\screenshot"

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
        self.selected_ip = ''
        self.ocr = ImgOCR()
        self.modbus_manager = ModbusManager()
        self.setup_modbus_manager = SetupModbusManager()
        self.meter_setup_process = DemoProcess()
        self.modbus_labels = ModbusLabels()
        self.touch_manager = TouchManager()
        self.evaluation = Evaluation()
        self.alarm = Alarm()
        self.stop_event = threading.Event()
        self.meter_demo_test = DemoTest(self.stop_event)
        self.setting_window = SettingWindow()
        self.setting_ip = SettingIP()
        
        self.tableWidget.setHorizontalHeaderLabels(["TITLE", "CONTENT", "RESULT (FAIL/TOTAL)"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(2, 250)
        
        self.setting_ip.ipSelected.connect(self.on_ip_selected)
        self.setting_ip.ipSelected.connect(self.setup_modbus_manager.ip_connect)
        self.setting_ip.tpSelected.connect(self.on_tp_selected)
        self.setting_ip.tpSelected.connect(self.setup_modbus_manager.tp_update)
        self.setting_ip.spSelected.connect(self.on_sp_selected)
        self.setting_ip.spSelected.connect(self.setup_modbus_manager.sp_update)

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

        self.btn_test_start.clicked.connect(self.test_start)
        self.btn_tc_save.clicked.connect(self.tc_save)
        self.btn_tc_load.clicked.connect(self.tc_load)

        self.debug_button.clicked.connect(self.debug_test)
        self.btn_setting.clicked.connect(self.ip_setting)
        self.btn_all_connect.clicked.connect(self.all_connect)
        self.btn_all_disconnect.clicked.connect(self.all_disconnect)

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
        
    def on_ip_selected(self, selected_ip):
        self.selected_ip = selected_ip
        print("대시보드에서 수신한 IP:", self.selected_ip)
        self.cur_ip = self.ip_display.setText(self.selected_ip)
        return self.selected_ip
    
    def on_tp_selected(self, selected_tp):
        print("대시보드에서 수신한 TP:", selected_tp)
        self.cur_tp = self.tp_display.setText(selected_tp)
        
    def on_sp_selected(self, selected_sp):
        print("대시보드에서 수신한 SP:", selected_sp)
        self.cur_sp = self.sp_display.setText(selected_sp) 

    # def on_current_checkbox_changed(self, state):
    #     if state == 2:
    #         self.current_checked = True
    #         print("Voltage checkbox checked")
    #     elif state == 0:
    #         self.current_checked = False
    #         print("Voltage checkbox unchecked")
    #     else:
    #         print(f"Unknown state: {state}")

    def switch_to_homePage(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_uiTestPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_setupTestPage(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_frameTestPage(self):
        self.stackedWidget.setCurrentIndex(3)
        
    def ip_setting(self):
        self.setting_ip.open_ip_window()
        
    def all_connect(self):
        self.setup_modbus_manager.tcp_connect()
        
    def all_disconnect(self):
        self.setup_modbus_manager.tcp_disconnect()

    def setup_connect(self):
        self.meter_setup_process.modbus_connect()

    def setup_disconnect(self):
        self.modbus_manager.tcp_disconnect()

    def select_webcam(self):
        self.webcam = WebCam()

    def start_webcam(self):
        self.webcam.start_streaming()

    def stop_webcam(self):
        self.webcam.stop_streaming()

    def stop_callback(self):
        return self.stop_thread
    
    def add_box_tc(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        for col in range(3):
            if col == 0:
                box_item = QTableWidgetItem()
                box_item.setFlags(box_item.flags() | Qt.ItemIsEditable)
                self.tableWidget.setItem(row_position, col, box_item)
            elif col == 1:
                box_item = QTableWidgetItem()
                box_item.setFlags(box_item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row_position, col, box_item)
            else:
                box_item = QTableWidgetItem()
                box_item.setFlags(box_item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row_position, col, box_item)
    
    def on_cell_double_click(self, row, col):
        if col == 1:
            if row not in self.set_windows:
                self.set_windows[row] = self.setting_window.open_new_window(row)
                self.set_windows[row].tcSelected.connect(self.on_tc_selected)
            self.set_windows[row].show()
        else:
            pass
    
    def on_tc_selected(self, row, text):
        print(f"on_tc_selected: row={row}, text={text}")
        item = QTableWidgetItem()
        item.setText(text)
        self.tableWidget.setItem(row, 1, item)

    def on_tc_score(self, row, text):
        print(f"on_tc_selected: row={row}, text={text}")
        item = QTableWidgetItem()
        item.setText(text)
        self.tableWidget.setItem(row, 2, item)

    def tc_save(self):
        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save Table Data",
            dir="",
            filter="XML Files (*.xml);;All Files (*)"
        )
        if filename:  # 사용자가 파일을 선택했다면
            self.save_table_to_xml(filename)
    
    def tc_load(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load Table Data",
            dir="",
            filter="XML Files (*.xml);;All Files (*)"
        )
        if filename:
            self.load_table_from_xml(filename)
        
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
        self.meter_demo_test.none_test_start()
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

    def test_start(self):
        self.worker = TestWorker(self.tableWidget, self)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()  # run() 비동기 실행

    def test_stop(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()

    def on_progress(self, row, content):
        print(f"[Progress] {row}행, content={content} 테스트 중...")

    def on_finished(self):
        print("테스트 스레드 종료/완료")

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
    
    def save_table_to_xml(self, filename):
        root = ET.Element("tableData")

        row_count = self.tableWidget.rowCount()
        col_count = self.tableWidget.columnCount()

        for r in range(row_count):
            # <row index="0"> ... </row>
            row_elem = ET.SubElement(root, "row", index=str(r))
            for c in range(col_count):
                item = self.tableWidget.item(r, c)
                text = item.text() if item else ""  # 아이템이 없는 셀도 있을 수 있음

                # <cell col="1"> 내용 </cell>
                cell_elem = ET.SubElement(row_elem, "cell", col=str(c))
                cell_elem.text = text

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] 테이블 데이터가 '{filename}' 파일에 저장되었습니다.")

    def load_table_from_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        self.tableWidget.setRowCount(0)

        for row_elem in root.findall("row"):
            r = int(row_elem.get("index"))
            # row가 부족하면 늘려둔다
            if r >= self.tableWidget.rowCount():
                self.tableWidget.setRowCount(r + 1)

            for cell_elem in row_elem.findall("cell"):
                c = int(cell_elem.get("col"))
                text = cell_elem.text if cell_elem.text else ""

                # 열 수도 부족하면 늘려야 함(혹은 이미 columnCount가 충분하다면 패스)
                if c >= self.tableWidget.columnCount():
                    # 예: columnCount가 3 이상 필요할 수 있음
                    self.tableWidget.setColumnCount(c + 1)

                item = QTableWidgetItem(text)
                self.tableWidget.setItem(r, c, item)

        print(f"[INFO] '{filename}' 파일에서 테이블 데이터가 로드되었습니다.")

class TestWorker(QThread):
    progress = Signal(int, str)  # (row, content) 진행 상황
    finished = Signal()          # 전체 테스트 완료 신호

    def __init__(self, tableWidget, dashboard_instance: MyDashBoard):
        super().__init__()
        self.tableWidget = tableWidget
        self.dashboard = dashboard_instance
        self.stopRequested = False
        self.stop_event = threading.Event()
        self.meter_demo_test = DemoTest(self.stop_event)
        self.search_pattern = os.path.join(image_directory, f'./**/*{self.dashboard.selected_ip}*.png')
        self.test_mode = None
        self.test_mode_setting = ModbusLabels()
        self.current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.base_save_path = os.path.expanduser(f"./results/{self.current_time}/")
        os.makedirs(self.base_save_path, exist_ok=True)
        self.test_map = {
            "tm_all": lambda: print("not yet"),
            "tm_balance": partial(self.execute_test_mode, self.meter_demo_test.demo_test_mode),
            "tm_noload": partial(self.execute_test_mode, self.meter_demo_test.noload_test_mode),
            "vol_all": lambda: self.meter_demo_test.demo_mea_vol_all(self.base_save_path, self.test_mode, self.search_pattern),
            "vol_rms": lambda: self.meter_demo_test.demo_mea_vol_rms(self.base_save_path, self.test_mode, self.search_pattern),
            "vol_fund": lambda: self.meter_demo_test.demo_mea_vol_fund(self.base_save_path, self.test_mode, self.search_pattern),
            "vol_thd": lambda: self.meter_demo_test.demo_mea_vol_thd(self.base_save_path, self.test_mode, self.search_pattern),
            "vol_freq": lambda: self.meter_demo_test.demo_mea_vol_freq(self.base_save_path, self.test_mode, self.search_pattern),
            "vol_residual": lambda: self.meter_demo_test.demo_mea_vol_residual(self.base_save_path, self.test_mode, self.search_pattern),
            "vol_sliding": lambda: self.meter_demo_test.demo_mea_vol_sliding(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_all": lambda: self.meter_demo_test.demo_mea_curr_all(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_rms": lambda: self.meter_demo_test.demo_mea_curr_rms(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_fund": lambda: self.meter_demo_test.demo_mea_curr_fund(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_demand": lambda: self.meter_demo_test.demo_mea_curr_demand(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_thd": lambda: self.meter_demo_test.demo_mea_curr_thd(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_tdd": lambda: self.meter_demo_test.demo_mea_curr_tdd(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_cf": lambda: self.meter_demo_test.demo_mea_curr_cf(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_kf": lambda: self.meter_demo_test.demo_mea_curr_kf(self.base_save_path, self.test_mode, self.search_pattern),
            "curr_residual": lambda: self.meter_demo_test.demo_mea_curr_residual(self.base_save_path, self.test_mode, self.search_pattern),
        }

        def result_callback(score, row):
            # 행의 RESULT 열에 결과 표시
            result_item = QTableWidgetItem(score)
            result_item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(row, 2, result_item)

        self.result_callback = result_callback 
    
    def execute_test_mode(self, mode_function):
        self.test_mode = mode_function()
        return self.test_mode

    def run(self):
        row_count = self.tableWidget.rowCount()

        for row in range(row_count):
            if self.stopRequested:
                print("STOP이 눌려 테스트 중단.")
                break

            content_item = self.tableWidget.item(row, 1)  # CONTENT 열
            if not content_item:
                continue

            content = content_item.text()
            self.progress.emit(row, content)  # 진행 상태 업데이트

            test_list = [x.strip() for x in content.split(",") if x.strip()]
            if not test_list:
                print("CONTENT가 비어있음")
                continue

            # DemoProcess 생성 및 실행
            
            demo_process = DemoProcess(
                score_callback=lambda score: self.result_callback(score, row)
            )
            for test_name in test_list:
                if test_name == "tm_balance":
                    # 이미 self.test_mode가 None이면 새로 세팅, 아니면 유지
                    self.execute_test_mode(self.meter_demo_test.demo_test_mode)
                    
                elif test_name == "tm_noload":
                 self.execute_test_mode(self.meter_demo_test.noload_test_mode)

            demo_process.demo_test_by_name(
                        test_name, self.base_save_path, self.test_mode, self.search_pattern
                    )
        
              
        # 모든 테스트 완료
        self.finished.emit()
        
    def stop(self):
        self.stopRequested = True

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