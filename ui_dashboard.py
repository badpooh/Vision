# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)
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
        icon.addFile(u":/images/dashboard.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.pushButton_3)

        self.btn_home_1 = QPushButton(self.icon_only_widget)
        self.btn_home_1.setObjectName(u"btn_home_1")
        icon1 = QIcon()
        icon1.addFile(u":/images/home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_home_1.setIcon(icon1)
        self.btn_home_1.setCheckable(True)
        self.btn_home_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_home_1)

        self.btn_ui_test_1 = QPushButton(self.icon_only_widget)
        self.btn_ui_test_1.setObjectName(u"btn_ui_test_1")
        icon2 = QIcon()
        icon2.addFile(u":/images/brand_family.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_ui_test_1.setIcon(icon2)
        self.btn_ui_test_1.setCheckable(True)
        self.btn_ui_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_ui_test_1)

        self.btn_setup_test_1 = QPushButton(self.icon_only_widget)
        self.btn_setup_test_1.setObjectName(u"btn_setup_test_1")
        icon3 = QIcon()
        icon3.addFile(u":/images/rule_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_setup_test_1.setIcon(icon3)
        self.btn_setup_test_1.setCheckable(True)
        self.btn_setup_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_setup_test_1)

        self.btn_frame_test_1 = QPushButton(self.icon_only_widget)
        self.btn_frame_test_1.setObjectName(u"btn_frame_test_1")
        icon4 = QIcon()
        icon4.addFile(u":/images/videocam.png", QSize(), QIcon.Normal, QIcon.Off)
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
        icon5.addFile(u":/images/logout.png", QSize(), QIcon.Normal, QIcon.Off)
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

        self.btn_setup_test_2 = QPushButton(self.icon_name_widget)
        self.btn_setup_test_2.setObjectName(u"btn_setup_test_2")
        self.btn_setup_test_2.setIcon(icon3)
        self.btn_setup_test_2.setCheckable(True)
        self.btn_setup_test_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_setup_test_2)

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
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 60, 480))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.tc_widget)


        self.gridLayout_3.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.ui_test_page)
        self.setup_test_page = QWidget()
        self.setup_test_page.setObjectName(u"setup_test_page")
        self.widget = QWidget(self.setup_test_page)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 20, 671, 661))
        self.btn_setup_test_start = QPushButton(self.setup_test_page)
        self.btn_setup_test_start.setObjectName(u"btn_setup_test_start")
        self.btn_setup_test_start.setGeometry(QRect(710, 70, 75, 24))
        self.btn_setup_test_stop = QPushButton(self.setup_test_page)
        self.btn_setup_test_stop.setObjectName(u"btn_setup_test_stop")
        self.btn_setup_test_stop.setGeometry(QRect(800, 70, 75, 24))
        self.btn_connect = QPushButton(self.setup_test_page)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setGeometry(QRect(710, 20, 75, 24))
        self.btn_disconnect = QPushButton(self.setup_test_page)
        self.btn_disconnect.setObjectName(u"btn_disconnect")
        self.btn_disconnect.setGeometry(QRect(800, 20, 75, 24))
        self.btn_setup_read = QPushButton(self.setup_test_page)
        self.btn_setup_read.setObjectName(u"btn_setup_read")
        self.btn_setup_read.setGeometry(QRect(710, 110, 75, 24))
        self.btn_FT_measurement = QPushButton(self.setup_test_page)
        self.btn_FT_measurement.setObjectName(u"btn_FT_measurement")
        self.btn_FT_measurement.setGeometry(QRect(720, 310, 121, 24))
        self.btn_FT_event = QPushButton(self.setup_test_page)
        self.btn_FT_event.setObjectName(u"btn_FT_event")
        self.btn_FT_event.setGeometry(QRect(720, 350, 121, 24))
        self.line = QFrame(self.setup_test_page)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(710, 280, 441, 16))
        font1 = QFont()
        font1.setBold(False)
        self.line.setFont(font1)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.btn_FT_network = QPushButton(self.setup_test_page)
        self.btn_FT_network.setObjectName(u"btn_FT_network")
        self.btn_FT_network.setGeometry(QRect(720, 390, 121, 24))
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
        self.btn_setup_test_1.toggled.connect(self.btn_setup_test_2.setChecked)
        self.btn_ui_test_1.toggled.connect(self.btn_ui_test_2.setChecked)
        self.btn_home_1.toggled.connect(self.btn_home_2.setChecked)
        self.btn_home_2.toggled.connect(self.btn_home_1.setChecked)
        self.btn_ui_test_2.toggled.connect(self.btn_ui_test_1.setChecked)
        self.btn_setup_test_2.toggled.connect(self.btn_setup_test_1.setChecked)
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
        self.btn_setup_test_2.setText(QCoreApplication.translate("MainWindow", u"SETUP TEST", None))
        self.btn_frame_test_2.setText(QCoreApplication.translate("MainWindow", u"FRAME TEST", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Sign Out", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"home", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.btn_add_tc.setText(QCoreApplication.translate("MainWindow", u"ADD TC", None))
        self.btn_setup_test_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_setup_test_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.btn_disconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.btn_setup_read.setText(QCoreApplication.translate("MainWindow", u"READ", None))
        self.btn_FT_measurement.setText(QCoreApplication.translate("MainWindow", u"F.T Measurement", None))
        self.btn_FT_event.setText(QCoreApplication.translate("MainWindow", u"F.T Event", None))
        self.btn_FT_network.setText(QCoreApplication.translate("MainWindow", u"F.T Network", None))
        self.btn_select_webcam.setText(QCoreApplication.translate("MainWindow", u"Select WebCam", None))
        self.btn_start_webcam.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btn_stop_webcam.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"focus_value", None))
    # retranslateUi

