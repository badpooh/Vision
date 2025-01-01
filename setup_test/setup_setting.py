from PySide6.QtWidgets import QVBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QTableWidgetItem, QTableWidget, QHeaderView
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression, Qt, Signal

from setup_test.ui_setting import Ui_Form
from setup_test.ui_setup_ip import Ui_setup_ip
from setup_test.setup_db import IPDataBase


class SettingWindow(QWidget, Ui_Form):
  
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.setObjectName("My Setting")
    self.widget_vol_checkBox.setHidden(True)
  
  def open_new_window(self, row):
    instance_qwidget = SettingWindow()
    instance_qwidget.setWindowTitle(f"Setting {row}")
    instance_qwidget.resize(600, 600)

    return instance_qwidget
  
class SettingIP(QWidget, Ui_setup_ip):
  
  ipSelected = Signal(str)
  
  def __init__(self):
    super().__init__()
    self.setObjectName("IP Setting")
    self.setupUi(self)
    regex = QRegularExpression(r"^[0-9.]*$")
    validator = QRegularExpressionValidator(regex, self)
    self.ip_typing.setValidator(validator)
    self.ip_list.verticalHeader().setVisible(False)
    self.ip_list.horizontalHeader().setVisible(False)
    self.ip_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    self.btn_ip_add.clicked.connect(self.add_ip)
    self.btn_ip_select.clicked.connect(self.select_ip)
    self.btn_ip_del.clicked.connect(self.del_ip)
    
    self.db = IPDataBase()
    
    self.load_ips()
        
  def open_ip_window(self):
    self.show()
    
  def load_ips(self):
    self.ip_list.setRowCount(0)

    all_ips = self.db.get_all_ips()
    for row_data in all_ips:
        ip_id = row_data[0]
        ip_value = row_data[1]

        row_position = self.ip_list.rowCount()
        self.ip_list.insertRow(row_position)

        item = QTableWidgetItem(ip_value)
        item.setTextAlignment(Qt.AlignCenter)

        # 편집 불가로 만들고 싶다면 플래그 조정
        # item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        self.ip_list.setItem(row_position, 0, item)
    
  def add_ip(self):
    typed_text = self.ip_typing.text()
    if not typed_text:
      return
    row_position = self.ip_list.rowCount()
    self.ip_list.insertRow(row_position)
    item = QTableWidgetItem(typed_text)
    item.setTextAlignment(Qt.AlignCenter)
    self.ip_list.setItem(row_position, 0, item)
    self.db.add_ip(typed_text)

    all_ips = self.db.get_all_ips()
    print("=== 현재 저장된 IP 목록 ===")
    for ip_row in all_ips:
        print(ip_row)  # (id, ip) 형태

  def select_ip(self):
    row = self.ip_list.currentRow()
    if row < 0:
        return

    item = self.ip_list.item(row, 0)
    if item:
        selected_ip = item.text()
        print(f"선택된 IP: {selected_ip}")
        self.ipSelected.emit(selected_ip)

  def del_ip(self):
    row = self.ip_list.currentRow()
    if row < 0:
        return

    item = self.ip_list.item(row, 0)
    if item:
        selected_ip = item.text()
        # 1) DB에서 삭제
        self.db.delete_ip(selected_ip)
        # 2) 테이블에서도 삭제
        self.ip_list.removeRow(row)
