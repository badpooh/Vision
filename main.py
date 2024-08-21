from PySide6.QtWidgets import QApplication
import sys
from dashboard import MyDashBoard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyDashBoard()
    window.show()
    sys.exit(app.exec())