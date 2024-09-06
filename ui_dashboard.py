# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1414, 731)
        MainWindow.setMinimumSize(QSize(1280, 720))
        MainWindow.setStyleSheet(u"background-color: rgb(245, 250, 254);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.icon_only_widget = QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName(u"icon_only_widget")
        self.icon_only_widget.setMinimumSize(QSize(0, 0))
        self.icon_only_widget.setMaximumSize(QSize(70, 16777215))
        self.icon_only_widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(175, 221, 236);\n"
"}\n"
"\n"
"QPushButton {\n"
"	color:black;\n"
"	text-align:center;\n"
"	height:30px;\n"
"	border:none;\n"
"	border-top-left-radius:10px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color:#F5FAFE;\n"
"	font-weight:bold;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.icon_only_widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(40, 40))
        self.label.setMaximumSize(QSize(40, 40))
        self.label.setPixmap(QPixmap(u":/images/Rootech.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.pushButton_3 = QPushButton(self.icon_only_widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        icon = QIcon()
        icon.addFile(u":/images/dashboard.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.pushButton_3)

        self.btn_home_1 = QPushButton(self.icon_only_widget)
        self.btn_home_1.setObjectName(u"btn_home_1")
        icon1 = QIcon()
        icon1.addFile(u":/images/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_home_1.setIcon(icon1)
        self.btn_home_1.setCheckable(True)
        self.btn_home_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_home_1)

        self.btn_ui_test_1 = QPushButton(self.icon_only_widget)
        self.btn_ui_test_1.setObjectName(u"btn_ui_test_1")
        icon2 = QIcon()
        icon2.addFile(u":/images/brand_family.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_ui_test_1.setIcon(icon2)
        self.btn_ui_test_1.setCheckable(True)
        self.btn_ui_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_ui_test_1)

        self.btn_setup_test_1 = QPushButton(self.icon_only_widget)
        self.btn_setup_test_1.setObjectName(u"btn_setup_test_1")
        icon3 = QIcon()
        icon3.addFile(u":/images/computer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_setup_test_1.setIcon(icon3)
        self.btn_setup_test_1.setCheckable(True)
        self.btn_setup_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_setup_test_1)

        self.btn_frame_test_1 = QPushButton(self.icon_only_widget)
        self.btn_frame_test_1.setObjectName(u"btn_frame_test_1")
        icon4 = QIcon()
        icon4.addFile(u":/images/videocam.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_frame_test_1.setIcon(icon4)
        self.btn_frame_test_1.setCheckable(True)
        self.btn_frame_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_frame_test_1)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 383, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.pushButton_6 = QPushButton(self.icon_only_widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        icon5 = QIcon()
        icon5.addFile(u":/images/logout.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setCheckable(True)

        self.verticalLayout_3.addWidget(self.pushButton_6)


        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)

        self.icon_name_widget = QWidget(self.centralwidget)
        self.icon_name_widget.setObjectName(u"icon_name_widget")
        self.icon_name_widget.setEnabled(True)
        self.icon_name_widget.setMinimumSize(QSize(0, 0))
        self.icon_name_widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(175, 221, 236);\n"
"}\n"
"\n"
"QPushButton {\n"
"	color:black;\n"
"	text-align:left;\n"
"	height:30px;\n"
"	border:none;\n"
"	padding-left:10px;\n"
"	border-top-left-radius:10px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color:#F5FAFE;\n"
"	font-weight:bold;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.icon_name_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.icon_name_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(40, 40))
        self.label_2.setMaximumSize(QSize(40, 40))
        self.label_2.setPixmap(QPixmap(u":/images/Rootech.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.icon_name_widget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        font.setBold(True)
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.pushButton_12 = QPushButton(self.icon_name_widget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setIcon(icon)
        self.pushButton_12.setCheckable(True)
        self.pushButton_12.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.pushButton_12)

        self.btn_home_2 = QPushButton(self.icon_name_widget)
        self.btn_home_2.setObjectName(u"btn_home_2")
        self.btn_home_2.setIcon(icon1)
        self.btn_home_2.setCheckable(True)
        self.btn_home_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_home_2)

        self.btn_ui_test_2 = QPushButton(self.icon_name_widget)
        self.btn_ui_test_2.setObjectName(u"btn_ui_test_2")
        self.btn_ui_test_2.setIcon(icon2)
        self.btn_ui_test_2.setCheckable(True)
        self.btn_ui_test_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_ui_test_2)

        self.btn_demo_test = QPushButton(self.icon_name_widget)
        self.btn_demo_test.setObjectName(u"btn_demo_test")
        self.btn_demo_test.setIcon(icon3)
        self.btn_demo_test.setCheckable(True)
        self.btn_demo_test.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_demo_test)

        self.btn_frame_test_2 = QPushButton(self.icon_name_widget)
        self.btn_frame_test_2.setObjectName(u"btn_frame_test_2")
        self.btn_frame_test_2.setIcon(icon4)
        self.btn_frame_test_2.setCheckable(True)
        self.btn_frame_test_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_frame_test_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 383, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.pushButton_7 = QPushButton(self.icon_name_widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setCheckable(True)

        self.verticalLayout_4.addWidget(self.pushButton_7)


        self.gridLayout.addWidget(self.icon_name_widget, 0, 1, 1, 1)

        self.main_menu = QWidget(self.centralwidget)
        self.main_menu.setObjectName(u"main_menu")
        self.verticalLayout_5 = QVBoxLayout(self.main_menu)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(self.main_menu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        font1 = QFont()
        font1.setPointSize(20)
        self.stackedWidget.setFont(font1)
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.label_4 = QLabel(self.home_page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 10, 48, 16))
        self.stackedWidget.addWidget(self.home_page)
        self.ui_test_page = QWidget()
        self.ui_test_page.setObjectName(u"ui_test_page")
        self.gridLayout_3 = QGridLayout(self.ui_test_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.menu_widget = QWidget(self.ui_test_page)
        self.menu_widget.setObjectName(u"menu_widget")
        self.menu_widget.setMinimumSize(QSize(1020, 100))
        self.menu_widget.setMaximumSize(QSize(500, 100))
        self.pushButton_2 = QPushButton(self.menu_widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(810, 50, 75, 24))
        self.btn_add_tc = QPushButton(self.menu_widget)
        self.btn_add_tc.setObjectName(u"btn_add_tc")
        self.btn_add_tc.setGeometry(QRect(910, 50, 75, 24))

        self.verticalLayout_6.addWidget(self.menu_widget)

        self.tc_widget = QWidget(self.ui_test_page)
        self.tc_widget.setObjectName(u"tc_widget")
        self.tc_widget.setMinimumSize(QSize(0, 500))
        self.gridLayout_2 = QGridLayout(self.tc_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(self.tc_widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.tc_widget)


        self.gridLayout_3.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.ui_test_page)
        self.setup_test_page = QWidget()
        self.setup_test_page.setObjectName(u"setup_test_page")
        self.btn_connect = QPushButton(self.setup_test_page)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setGeometry(QRect(190, 30, 101, 31))
        self.btn_connect.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        background-color: #f0f0f0;\n"
"        padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.btn_connect.setAutoDefault(False)
        self.btn_connect.setFlat(False)
        self.btn_disconnect = QPushButton(self.setup_test_page)
        self.btn_disconnect.setObjectName(u"btn_disconnect")
        self.btn_disconnect.setGeometry(QRect(310, 30, 91, 31))
        self.btn_disconnect.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        background-color: #f0f0f0;\n"
"        padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.line = QFrame(self.setup_test_page)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 80, 1151, 16))
        font2 = QFont()
        font2.setBold(False)
        self.line.setFont(font2)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.btn_demo_mode_ui_test = QPushButton(self.setup_test_page)
        self.btn_demo_mode_ui_test.setObjectName(u"btn_demo_mode_ui_test")
        self.btn_demo_mode_ui_test.setGeometry(QRect(190, 110, 121, 41))
        self.btn_demo_mode_ui_test.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        background-color: #f0f0f0;\n"
"        padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.checkBox_voltage = QCheckBox(self.setup_test_page)
        self.checkBox_voltage.setObjectName(u"checkBox_voltage")
        self.checkBox_voltage.setGeometry(QRect(20, 120, 79, 20))
        self.checkBox_current = QCheckBox(self.setup_test_page)
        self.checkBox_current.setObjectName(u"checkBox_current")
        self.checkBox_current.setGeometry(QRect(20, 160, 79, 20))
        self.checkBox_power = QCheckBox(self.setup_test_page)
        self.checkBox_power.setObjectName(u"checkBox_power")
        self.checkBox_power.setGeometry(QRect(20, 200, 79, 20))
        self.checkBox_analysis = QCheckBox(self.setup_test_page)
        self.checkBox_analysis.setObjectName(u"checkBox_analysis")
        self.checkBox_analysis.setGeometry(QRect(20, 240, 79, 20))
        self.debug_button = QPushButton(self.setup_test_page)
        self.debug_button.setObjectName(u"debug_button")
        self.debug_button.setGeometry(QRect(1000, 630, 141, 51))
        self.btn_demo_mode_ui_test_2 = QPushButton(self.setup_test_page)
        self.btn_demo_mode_ui_test_2.setObjectName(u"btn_demo_mode_ui_test_2")
        self.btn_demo_mode_ui_test_2.setGeometry(QRect(190, 170, 121, 41))
        self.btn_demo_mode_ui_test_2.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        background-color: #f0f0f0;\n"
"        padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.input_ip = QLineEdit(self.setup_test_page)
        self.input_ip.setObjectName(u"input_ip")
        self.input_ip.setGeometry(QRect(10, 30, 151, 31))
        font3 = QFont()
        font3.setPointSize(12)
        self.input_ip.setFont(font3)
        self.score = QLabel(self.setup_test_page)
        self.score.setObjectName(u"score")
        self.score.setGeometry(QRect(370, 150, 131, 81))
        font4 = QFont()
        font4.setPointSize(25)
        self.score.setFont(font4)
        self.score.setFrameShape(QFrame.Shape.Box)
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score.setWordWrap(False)
        self.score_label = QLabel(self.setup_test_page)
        self.score_label.setObjectName(u"score_label")
        self.score_label.setGeometry(QRect(380, 120, 111, 16))
        self.stackedWidget.addWidget(self.setup_test_page)
        self.frame_test_page = QWidget()
        self.frame_test_page.setObjectName(u"frame_test_page")
        self.btn_select_webcam = QPushButton(self.frame_test_page)
        self.btn_select_webcam.setObjectName(u"btn_select_webcam")
        self.btn_select_webcam.setGeometry(QRect(20, 30, 101, 31))
        self.btn_select_webcam.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid black;\n"
"}")
        self.btn_select_webcam.setCheckable(True)
        self.btn_start_webcam = QPushButton(self.frame_test_page)
        self.btn_start_webcam.setObjectName(u"btn_start_webcam")
        self.btn_start_webcam.setGeometry(QRect(30, 90, 75, 24))
        self.btn_stop_webcam = QPushButton(self.frame_test_page)
        self.btn_stop_webcam.setObjectName(u"btn_stop_webcam")
        self.btn_stop_webcam.setGeometry(QRect(120, 90, 75, 24))
        self.label_5 = QLabel(self.frame_test_page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(40, 140, 71, 16))
        self.lineEdit = QLineEdit(self.frame_test_page)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(40, 170, 113, 31))
        self.stackedWidget.addWidget(self.frame_test_page)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.stackedWidget.addWidget(self.page_5)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.gridLayout.addWidget(self.main_menu, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.btn_frame_test_1.toggled.connect(self.btn_frame_test_2.setChecked)
        self.btn_setup_test_1.toggled.connect(self.btn_demo_test.setChecked)
        self.btn_ui_test_1.toggled.connect(self.btn_ui_test_2.setChecked)
        self.btn_home_1.toggled.connect(self.btn_home_2.setChecked)
        self.btn_home_2.toggled.connect(self.btn_home_1.setChecked)
        self.btn_ui_test_2.toggled.connect(self.btn_ui_test_1.setChecked)
        self.btn_demo_test.toggled.connect(self.btn_setup_test_1.setChecked)
        self.btn_frame_test_2.toggled.connect(self.btn_frame_test_1.setChecked)
        self.pushButton_6.toggled.connect(MainWindow.close)
        self.pushButton_7.toggled.connect(MainWindow.close)
        self.pushButton_12.toggled.connect(self.pushButton_3.setChecked)
        self.pushButton_12.clicked["bool"].connect(self.icon_only_widget.setVisible)
        self.pushButton_12.clicked["bool"].connect(self.icon_name_widget.setHidden)
        self.pushButton_3.toggled.connect(self.pushButton_12.setChecked)
        self.pushButton_3.clicked["bool"].connect(self.icon_only_widget.setHidden)
        self.pushButton_3.clicked["bool"].connect(self.icon_name_widget.setVisible)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.pushButton_3.setText("")
        self.btn_home_1.setText("")
        self.btn_ui_test_1.setText("")
        self.btn_setup_test_1.setText("")
        self.btn_frame_test_1.setText("")
        self.pushButton_6.setText("")
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ROOTECH", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"DASHBOARD", None))
        self.btn_home_2.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.btn_ui_test_2.setText(QCoreApplication.translate("MainWindow", u"UI TEST", None))
        self.btn_demo_test.setText(QCoreApplication.translate("MainWindow", u"DEMO TEST", None))
        self.btn_frame_test_2.setText(QCoreApplication.translate("MainWindow", u"FRAME TEST", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Sign Out", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"home", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.btn_add_tc.setText(QCoreApplication.translate("MainWindow", u"ADD TC", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.btn_disconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.btn_demo_mode_ui_test.setText(QCoreApplication.translate("MainWindow", u"Demo Mode \n"
"UI TEST START ", None))
        self.checkBox_voltage.setText(QCoreApplication.translate("MainWindow", u"VOLTAGE", None))
        self.checkBox_current.setText(QCoreApplication.translate("MainWindow", u"CURRENT", None))
        self.checkBox_power.setText(QCoreApplication.translate("MainWindow", u"POWER", None))
        self.checkBox_analysis.setText(QCoreApplication.translate("MainWindow", u"ANALYSIS", None))
        self.debug_button.setText(QCoreApplication.translate("MainWindow", u"Debug Button", None))
        self.btn_demo_mode_ui_test_2.setText(QCoreApplication.translate("MainWindow", u"Demo Mode \n"
"UI TEST STOP", None))
        self.input_ip.setInputMask("")
        self.input_ip.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter IP address", None))
        self.score.setText("")
        self.score_label.setText(QCoreApplication.translate("MainWindow", u"RESULT (FAIL/TOTAL)", None))
        self.btn_select_webcam.setText(QCoreApplication.translate("MainWindow", u"Select WebCam", None))
        self.btn_start_webcam.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btn_stop_webcam.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"focus_value", None))
    # retranslateUi

