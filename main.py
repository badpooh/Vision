from PySide6.QtWidgets import QApplication
import sys

from dashboard import MyDashBoard
from setup_test.setup_process import SetupTest

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = MyDashBoard()
    setup = SetupTest(dashboard)
    dashboard.show()
    sys.exit(app.exec())