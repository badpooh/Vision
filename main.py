from PySide6.QtWidgets import QApplication
import sys

from dashboard import MyDashBoard
from setup_test.setup_process import SetupTest

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # SetupTest 객체 먼저 생성
    setup_test = SetupTest()

    # MyDashBoard 생성 시 setup_test 객체 전달
    dashboard = MyDashBoard(setup_test_instance=setup_test)
    dashboard.cb_AccuraSMChanged.connect(setup_test.on_accurasm_checked)
    dashboard.show()
    sys.exit(app.exec())