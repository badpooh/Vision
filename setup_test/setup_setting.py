from PySide6.QtWidgets import QVBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class SettingWindow:
  
    # open_new_window 메서드 수정
  def open_new_window(self, row):
    dialog = QDialog(parent=self if isinstance(self, QWidget) else None)  
    dialog.setWindowTitle(f"Setting {row}")
    dialog.resize(600, 600)
    
    layout = QVBoxLayout()
    
    # 창에서 사용할 입력 필드
    label = QLabel(f"Edit data for row {row}")
    layout.addWidget(label)
    
    # 입력 필드 (나중에 데이터베이스와 연결 가능)
    self.input_field = QLineEdit()
    layout.addWidget(self.input_field)

    # 저장 버튼
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_data(row))
    layout.addWidget(save_button)
    
    dialog.setLayout(layout)
    return dialog
