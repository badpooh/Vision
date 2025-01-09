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
   
	def open_new_window(self, row):
		instance_qwidget = SettingWindow()
		instance_qwidget.setWindowTitle(f"Setting {row}")
		instance_qwidget.resize(600, 600)

		return instance_qwidget
	
class SettingIP(QWidget, Ui_setup_ip):
	
	ipSelected = Signal(str)
	tpSelected = Signal(str)
	spSelected = Signal(str)
	
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
		self.btn_tp_add.clicked.connect(self.add_touch_port)
		self.btn_tp_select.clicked.connect(self.select_touch_port)
		self.btn_tp_del.clicked.connect(self.del_touch_port)
		self.btn_sp_add.clicked.connect(self.add_setup_port)
		self.btn_sp_select.clicked.connect(self.select_setup_port)
		self.btn_sp_del.clicked.connect(self.del_setup_port)
		
		self.db = IPDataBase()
		
		self.load_ips()
			
	def open_ip_window(self):
		self.show()
		
	def load_ips(self):
		self.ip_list.setRowCount(0)
		self.tp_list.setRowCount(0)
		self.sp_list.setRowCount(0)

		all_data = self.db.get_all_ips()
		
		for row_data in all_data:
			row_id, row_type, row_value = row_data  # 예: (1, 'ip', '10.10.10.1')

			if row_type == 'ip':
				ip_row_position = self.ip_list.rowCount()
				self.ip_list.insertRow(ip_row_position)

				ip_item = QTableWidgetItem(row_value)
				ip_item.setTextAlignment(Qt.AlignCenter)
				self.ip_list.setItem(ip_row_position, 0, ip_item)

			elif row_type == 'tp':
				tp_row_position = self.tp_list.rowCount()
				self.tp_list.insertRow(tp_row_position)

				tp_item = QTableWidgetItem(row_value)
				tp_item.setTextAlignment(Qt.AlignCenter)
				self.tp_list.setItem(tp_row_position, 0, tp_item)

			elif row_type == 'sp':
				sp_row_position = self.sp_list.rowCount()
				self.sp_list.insertRow(sp_row_position)

				sp_item = QTableWidgetItem(row_value)
				sp_item.setTextAlignment(Qt.AlignCenter)
				self.sp_list.setItem(sp_row_position, 0, sp_item)

			else:
				print(f"알 수 없는 type: {row_type}, value: {row_value}")
			
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
			
	def add_touch_port(self):
		typed_text = self.tp_typing.text()
		if not typed_text:
			return
		row_position = self.tp_list.rowCount()
		self.tp_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.tp_list.setItem(row_position, 0, item)
		self.db.add_touch_port(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태
			
	def select_touch_port(self):
		row = self.tp_list.currentRow()
		if row < 0:
			return

		item = self.tp_list.item(row, 0)
		if item:
			selected_tp = item.text()
			print(f"선택된 TP: {selected_tp}")
			self.tpSelected.emit(selected_tp)
	
	def del_touch_port(self):
		row = self.tp_list.currentRow()
		if row < 0:
			return

		item = self.tp_list.item(row, 0)
		if item:
			selected_tp = item.text()
			self.db.delete_ip(selected_tp)
			self.tp_list.removeRow(row)
	
	def add_setup_port(self):
		typed_text = self.sp_typing.text()
		if not typed_text:
			return
		row_position = self.sp_list.rowCount()
		self.sp_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.sp_list.setItem(row_position, 0, item)
		self.db.add_setup_port(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태
			
	def select_setup_port(self):
		row = self.sp_list.currentRow()
		if row < 0:
			return

		item = self.sp_list.item(row, 0)
		if item:
			selected_sp = item.text()
			print(f"선택된 SP: {selected_sp}")
			self.spSelected.emit(selected_sp)
	
	def del_setup_port(self):
		row = self.sp_list.currentRow()
		if row < 0:
			return

		item = self.sp_list.item(row, 0)
		if item:
			selected_sp = item.text()
			self.db.delete_ip(selected_sp)
			self.sp_list.removeRow(row)
