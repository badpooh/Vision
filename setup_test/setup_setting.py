from PySide6.QtWidgets import QVBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from setup_test.ui_setting import Ui_Form


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

