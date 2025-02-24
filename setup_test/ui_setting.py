# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(837, 769)
        Form.setMinimumSize(QSize(800, 600))
        Form.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 771, 581))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.gridLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(20, 20, 746, 551))
        self.widget_2.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.btn_apply = QPushButton(self.widget_2)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setGeometry(QRect(520, 450, 75, 24))
        self.btn_cancel = QPushButton(self.widget_2)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(605, 450, 75, 24))
        self.main_menu1 = QWidget(self.widget_2)
        self.main_menu1.setObjectName(u"main_menu1")
        self.main_menu1.setGeometry(QRect(10, 20, 174, 408))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_menu1.sizePolicy().hasHeightForWidth())
        self.main_menu1.setSizePolicy(sizePolicy)
        self.main_menu1.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.formLayout = QFormLayout(self.main_menu1)
        self.formLayout.setObjectName(u"formLayout")
        self.sub_menu1 = QWidget(self.main_menu1)
        self.sub_menu1.setObjectName(u"sub_menu1")
        self.sub_menu1.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"")
        self.verticalLayout_7 = QVBoxLayout(self.sub_menu1)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.sub_box1 = QVBoxLayout()
        self.sub_box1.setObjectName(u"sub_box1")
        self.btn_menu_voltage = QPushButton(self.sub_menu1)
        self.btn_menu_voltage.setObjectName(u"btn_menu_voltage")
        sizePolicy.setHeightForWidth(self.btn_menu_voltage.sizePolicy().hasHeightForWidth())
        self.btn_menu_voltage.setSizePolicy(sizePolicy)
        self.btn_menu_voltage.setMinimumSize(QSize(130, 24))
        self.btn_menu_voltage.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_voltage.setStyleSheet(u"QPushButton:checked {\n"
"  background-color: #d0d0d0;\n"
"}")
        self.btn_menu_voltage.setCheckable(True)
        self.btn_menu_voltage.setChecked(False)
        self.btn_menu_voltage.setAutoDefault(False)
        self.btn_menu_voltage.setFlat(False)

        self.sub_box1.addWidget(self.btn_menu_voltage)

        self.vol_check_box = QWidget(self.sub_menu1)
        self.vol_check_box.setObjectName(u"vol_check_box")
        sizePolicy.setHeightForWidth(self.vol_check_box.sizePolicy().hasHeightForWidth())
        self.vol_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.vol_check_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cb_vol_all = QCheckBox(self.vol_check_box)
        self.cb_vol_all.setObjectName(u"cb_vol_all")

        self.verticalLayout.addWidget(self.cb_vol_all)

        self.cb_vol_rms = QCheckBox(self.vol_check_box)
        self.cb_vol_rms.setObjectName(u"cb_vol_rms")

        self.verticalLayout.addWidget(self.cb_vol_rms)

        self.cb_vol_fund = QCheckBox(self.vol_check_box)
        self.cb_vol_fund.setObjectName(u"cb_vol_fund")

        self.verticalLayout.addWidget(self.cb_vol_fund)

        self.cb_vol_thd = QCheckBox(self.vol_check_box)
        self.cb_vol_thd.setObjectName(u"cb_vol_thd")

        self.verticalLayout.addWidget(self.cb_vol_thd)

        self.cb_vol_freq = QCheckBox(self.vol_check_box)
        self.cb_vol_freq.setObjectName(u"cb_vol_freq")

        self.verticalLayout.addWidget(self.cb_vol_freq)

        self.cb_vol_residual = QCheckBox(self.vol_check_box)
        self.cb_vol_residual.setObjectName(u"cb_vol_residual")

        self.verticalLayout.addWidget(self.cb_vol_residual)

        self.cb_vol_sliding = QCheckBox(self.vol_check_box)
        self.cb_vol_sliding.setObjectName(u"cb_vol_sliding")

        self.verticalLayout.addWidget(self.cb_vol_sliding)


        self.sub_box1.addWidget(self.vol_check_box)


        self.verticalLayout_7.addLayout(self.sub_box1)


        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.sub_menu1)

        self.sub_menu2 = QWidget(self.main_menu1)
        self.sub_menu2.setObjectName(u"sub_menu2")
        self.sub_menu2.setMinimumSize(QSize(120, 0))
        self.sub_menu2.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.verticalLayout_8 = QVBoxLayout(self.sub_menu2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.sub_box2 = QVBoxLayout()
        self.sub_box2.setObjectName(u"sub_box2")
        self.btn_menu_test_mode = QPushButton(self.sub_menu2)
        self.btn_menu_test_mode.setObjectName(u"btn_menu_test_mode")
        sizePolicy.setHeightForWidth(self.btn_menu_test_mode.sizePolicy().hasHeightForWidth())
        self.btn_menu_test_mode.setSizePolicy(sizePolicy)
        self.btn_menu_test_mode.setMinimumSize(QSize(130, 24))
        self.btn_menu_test_mode.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_test_mode.setCheckable(True)
        self.btn_menu_test_mode.setChecked(False)
        self.btn_menu_test_mode.setAutoDefault(False)
        self.btn_menu_test_mode.setFlat(False)

        self.sub_box2.addWidget(self.btn_menu_test_mode)

        self.tm_check_box = QWidget(self.sub_menu2)
        self.tm_check_box.setObjectName(u"tm_check_box")
        sizePolicy.setHeightForWidth(self.tm_check_box.sizePolicy().hasHeightForWidth())
        self.tm_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.tm_check_box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.cb_tm_all = QCheckBox(self.tm_check_box)
        self.cb_tm_all.setObjectName(u"cb_tm_all")

        self.verticalLayout_6.addWidget(self.cb_tm_all)

        self.cb_tm_balance = QCheckBox(self.tm_check_box)
        self.cb_tm_balance.setObjectName(u"cb_tm_balance")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cb_tm_balance.sizePolicy().hasHeightForWidth())
        self.cb_tm_balance.setSizePolicy(sizePolicy1)

        self.verticalLayout_6.addWidget(self.cb_tm_balance)

        self.cb_tm_noload = QCheckBox(self.tm_check_box)
        self.cb_tm_noload.setObjectName(u"cb_tm_noload")

        self.verticalLayout_6.addWidget(self.cb_tm_noload)


        self.sub_box2.addWidget(self.tm_check_box)


        self.verticalLayout_8.addLayout(self.sub_box2)


        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.sub_menu2)

        self.main_menu2 = QWidget(self.widget_2)
        self.main_menu2.setObjectName(u"main_menu2")
        self.main_menu2.setGeometry(QRect(145, 20, 174, 296))
        sizePolicy.setHeightForWidth(self.main_menu2.sizePolicy().hasHeightForWidth())
        self.main_menu2.setSizePolicy(sizePolicy)
        self.main_menu2.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"\n"
"\n"
"")
        self.formLayout_2 = QFormLayout(self.main_menu2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.sub_menu3 = QWidget(self.main_menu2)
        self.sub_menu3.setObjectName(u"sub_menu3")
        self.sub_menu3.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.verticalLayout_9 = QVBoxLayout(self.sub_menu3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.sub_box3 = QVBoxLayout()
        self.sub_box3.setObjectName(u"sub_box3")
        self.btn_menu_current = QPushButton(self.sub_menu3)
        self.btn_menu_current.setObjectName(u"btn_menu_current")
        sizePolicy.setHeightForWidth(self.btn_menu_current.sizePolicy().hasHeightForWidth())
        self.btn_menu_current.setSizePolicy(sizePolicy)
        self.btn_menu_current.setMinimumSize(QSize(130, 24))
        self.btn_menu_current.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_current.setCheckable(True)
        self.btn_menu_current.setChecked(False)
        self.btn_menu_current.setAutoDefault(False)
        self.btn_menu_current.setFlat(False)

        self.sub_box3.addWidget(self.btn_menu_current)

        self.curr_check_box = QWidget(self.sub_menu3)
        self.curr_check_box.setObjectName(u"curr_check_box")
        sizePolicy.setHeightForWidth(self.curr_check_box.sizePolicy().hasHeightForWidth())
        self.curr_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_10 = QVBoxLayout(self.curr_check_box)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.cb_curr_all = QCheckBox(self.curr_check_box)
        self.cb_curr_all.setObjectName(u"cb_curr_all")
        self.cb_curr_all.setCheckable(True)
        self.cb_curr_all.setChecked(False)

        self.verticalLayout_10.addWidget(self.cb_curr_all)

        self.cb_curr_rms = QCheckBox(self.curr_check_box)
        self.cb_curr_rms.setObjectName(u"cb_curr_rms")

        self.verticalLayout_10.addWidget(self.cb_curr_rms)

        self.cb_curr_fund = QCheckBox(self.curr_check_box)
        self.cb_curr_fund.setObjectName(u"cb_curr_fund")

        self.verticalLayout_10.addWidget(self.cb_curr_fund)

        self.cb_curr_demand = QCheckBox(self.curr_check_box)
        self.cb_curr_demand.setObjectName(u"cb_curr_demand")

        self.verticalLayout_10.addWidget(self.cb_curr_demand)

        self.cb_curr_thd = QCheckBox(self.curr_check_box)
        self.cb_curr_thd.setObjectName(u"cb_curr_thd")

        self.verticalLayout_10.addWidget(self.cb_curr_thd)

        self.cb_curr_tdd = QCheckBox(self.curr_check_box)
        self.cb_curr_tdd.setObjectName(u"cb_curr_tdd")

        self.verticalLayout_10.addWidget(self.cb_curr_tdd)

        self.cb_curr_cf = QCheckBox(self.curr_check_box)
        self.cb_curr_cf.setObjectName(u"cb_curr_cf")

        self.verticalLayout_10.addWidget(self.cb_curr_cf)

        self.cb_curr_kf = QCheckBox(self.curr_check_box)
        self.cb_curr_kf.setObjectName(u"cb_curr_kf")

        self.verticalLayout_10.addWidget(self.cb_curr_kf)

        self.cb_curr_residual = QCheckBox(self.curr_check_box)
        self.cb_curr_residual.setObjectName(u"cb_curr_residual")

        self.verticalLayout_10.addWidget(self.cb_curr_residual)


        self.sub_box3.addWidget(self.curr_check_box)


        self.verticalLayout_9.addLayout(self.sub_box3)


        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.sub_menu3)

        self.main_menu3 = QWidget(self.widget_2)
        self.main_menu3.setObjectName(u"main_menu3")
        self.main_menu3.setGeometry(QRect(280, 20, 174, 296))
        sizePolicy.setHeightForWidth(self.main_menu3.sizePolicy().hasHeightForWidth())
        self.main_menu3.setSizePolicy(sizePolicy)
        self.main_menu3.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"\n"
"\n"
"")
        self.formLayout_3 = QFormLayout(self.main_menu3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.sub_menu4 = QWidget(self.main_menu3)
        self.sub_menu4.setObjectName(u"sub_menu4")
        self.sub_menu4.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.verticalLayout_11 = QVBoxLayout(self.sub_menu4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.sub_box4 = QVBoxLayout()
        self.sub_box4.setObjectName(u"sub_box4")
        self.btn_menu_power = QPushButton(self.sub_menu4)
        self.btn_menu_power.setObjectName(u"btn_menu_power")
        sizePolicy.setHeightForWidth(self.btn_menu_power.sizePolicy().hasHeightForWidth())
        self.btn_menu_power.setSizePolicy(sizePolicy)
        self.btn_menu_power.setMinimumSize(QSize(130, 24))
        self.btn_menu_power.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_power.setCheckable(True)
        self.btn_menu_power.setChecked(False)
        self.btn_menu_power.setAutoDefault(False)
        self.btn_menu_power.setFlat(False)

        self.sub_box4.addWidget(self.btn_menu_power)

        self.pow_check_box = QWidget(self.sub_menu4)
        self.pow_check_box.setObjectName(u"pow_check_box")
        sizePolicy.setHeightForWidth(self.pow_check_box.sizePolicy().hasHeightForWidth())
        self.pow_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_12 = QVBoxLayout(self.pow_check_box)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.cb_pow_all = QCheckBox(self.pow_check_box)
        self.cb_pow_all.setObjectName(u"cb_pow_all")
        self.cb_pow_all.setCheckable(True)
        self.cb_pow_all.setChecked(False)

        self.verticalLayout_12.addWidget(self.cb_pow_all)

        self.cb_pow_p = QCheckBox(self.pow_check_box)
        self.cb_pow_p.setObjectName(u"cb_pow_p")

        self.verticalLayout_12.addWidget(self.cb_pow_p)

        self.cb_pow_q = QCheckBox(self.pow_check_box)
        self.cb_pow_q.setObjectName(u"cb_pow_q")

        self.verticalLayout_12.addWidget(self.cb_pow_q)

        self.cb_pow_s = QCheckBox(self.pow_check_box)
        self.cb_pow_s.setObjectName(u"cb_pow_s")

        self.verticalLayout_12.addWidget(self.cb_pow_s)

        self.cb_pow_pf = QCheckBox(self.pow_check_box)
        self.cb_pow_pf.setObjectName(u"cb_pow_pf")

        self.verticalLayout_12.addWidget(self.cb_pow_pf)

        self.cb_pow_demand = QCheckBox(self.pow_check_box)
        self.cb_pow_demand.setObjectName(u"cb_pow_demand")

        self.verticalLayout_12.addWidget(self.cb_pow_demand)

        self.cb_pow_energy = QCheckBox(self.pow_check_box)
        self.cb_pow_energy.setObjectName(u"cb_pow_energy")

        self.verticalLayout_12.addWidget(self.cb_pow_energy)


        self.sub_box4.addWidget(self.pow_check_box)


        self.verticalLayout_11.addLayout(self.sub_box4)


        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.sub_menu4)

        self.main_menu4 = QWidget(self.widget_2)
        self.main_menu4.setObjectName(u"main_menu4")
        self.main_menu4.setGeometry(QRect(415, 20, 174, 381))
        sizePolicy.setHeightForWidth(self.main_menu4.sizePolicy().hasHeightForWidth())
        self.main_menu4.setSizePolicy(sizePolicy)
        self.main_menu4.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.formLayout_4 = QFormLayout(self.main_menu4)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.sub_menu5 = QWidget(self.main_menu4)
        self.sub_menu5.setObjectName(u"sub_menu5")
        self.sub_menu5.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"")
        self.verticalLayout_13 = QVBoxLayout(self.sub_menu5)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.sub_box5 = QVBoxLayout()
        self.sub_box5.setObjectName(u"sub_box5")
        self.btn_menu_analysis = QPushButton(self.sub_menu5)
        self.btn_menu_analysis.setObjectName(u"btn_menu_analysis")
        sizePolicy.setHeightForWidth(self.btn_menu_analysis.sizePolicy().hasHeightForWidth())
        self.btn_menu_analysis.setSizePolicy(sizePolicy)
        self.btn_menu_analysis.setMinimumSize(QSize(130, 24))
        self.btn_menu_analysis.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_analysis.setCheckable(True)
        self.btn_menu_analysis.setChecked(False)
        self.btn_menu_analysis.setAutoDefault(False)
        self.btn_menu_analysis.setFlat(False)

        self.sub_box5.addWidget(self.btn_menu_analysis)

        self.anal_check_box = QWidget(self.sub_menu5)
        self.anal_check_box.setObjectName(u"anal_check_box")
        sizePolicy.setHeightForWidth(self.anal_check_box.sizePolicy().hasHeightForWidth())
        self.anal_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.anal_check_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cb_anal_all = QCheckBox(self.anal_check_box)
        self.cb_anal_all.setObjectName(u"cb_anal_all")

        self.verticalLayout_2.addWidget(self.cb_anal_all)

        self.cb_anal_phasor = QCheckBox(self.anal_check_box)
        self.cb_anal_phasor.setObjectName(u"cb_anal_phasor")

        self.verticalLayout_2.addWidget(self.cb_anal_phasor)

        self.cb_anal_harmonics = QCheckBox(self.anal_check_box)
        self.cb_anal_harmonics.setObjectName(u"cb_anal_harmonics")

        self.verticalLayout_2.addWidget(self.cb_anal_harmonics)

        self.cb_anal_waveform = QCheckBox(self.anal_check_box)
        self.cb_anal_waveform.setObjectName(u"cb_anal_waveform")

        self.verticalLayout_2.addWidget(self.cb_anal_waveform)

        self.cb_anal_volt_sym = QCheckBox(self.anal_check_box)
        self.cb_anal_volt_sym.setObjectName(u"cb_anal_volt_sym")

        self.verticalLayout_2.addWidget(self.cb_anal_volt_sym)

        self.cb_anal_volt_unbal = QCheckBox(self.anal_check_box)
        self.cb_anal_volt_unbal.setObjectName(u"cb_anal_volt_unbal")

        self.verticalLayout_2.addWidget(self.cb_anal_volt_unbal)

        self.cb_anal_curr_sym = QCheckBox(self.anal_check_box)
        self.cb_anal_curr_sym.setObjectName(u"cb_anal_curr_sym")

        self.verticalLayout_2.addWidget(self.cb_anal_curr_sym)

        self.cb_anal_curr_unbal = QCheckBox(self.anal_check_box)
        self.cb_anal_curr_unbal.setObjectName(u"cb_anal_curr_unbal")

        self.verticalLayout_2.addWidget(self.cb_anal_curr_unbal)


        self.sub_box5.addWidget(self.anal_check_box)


        self.verticalLayout_13.addLayout(self.sub_box5)


        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.sub_menu5)

        self.sub_menu6 = QWidget(self.main_menu4)
        self.sub_menu6.setObjectName(u"sub_menu6")
        self.sub_menu6.setMinimumSize(QSize(120, 0))
        self.sub_menu6.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.verticalLayout_14 = QVBoxLayout(self.sub_menu6)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.sub_box6 = QVBoxLayout()
        self.sub_box6.setObjectName(u"sub_box6")
        self.btn_menu_system = QPushButton(self.sub_menu6)
        self.btn_menu_system.setObjectName(u"btn_menu_system")
        sizePolicy.setHeightForWidth(self.btn_menu_system.sizePolicy().hasHeightForWidth())
        self.btn_menu_system.setSizePolicy(sizePolicy)
        self.btn_menu_system.setMinimumSize(QSize(130, 24))
        self.btn_menu_system.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_system.setCheckable(True)
        self.btn_menu_system.setChecked(False)
        self.btn_menu_system.setAutoDefault(False)
        self.btn_menu_system.setFlat(False)

        self.sub_box6.addWidget(self.btn_menu_system)

        self.sys_check_box = QWidget(self.sub_menu6)
        self.sys_check_box.setObjectName(u"sys_check_box")
        sizePolicy.setHeightForWidth(self.sys_check_box.sizePolicy().hasHeightForWidth())
        self.sys_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_15 = QVBoxLayout(self.sys_check_box)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.cb_sys_all = QCheckBox(self.sys_check_box)
        self.cb_sys_all.setObjectName(u"cb_sys_all")

        self.verticalLayout_15.addWidget(self.cb_sys_all)


        self.sub_box6.addWidget(self.sys_check_box)


        self.verticalLayout_14.addLayout(self.sub_box6)


        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.sub_menu6)

        self.sub_menu7 = QWidget(self.widget_2)
        self.sub_menu7.setObjectName(u"sub_menu7")
        self.sub_menu7.setGeometry(QRect(590, 35, 150, 140))
        self.sub_menu7.setMinimumSize(QSize(120, 0))
        self.sub_menu7.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.verticalLayout_16 = QVBoxLayout(self.sub_menu7)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.sub_box6_2 = QVBoxLayout()
        self.sub_box6_2.setObjectName(u"sub_box6_2")
        self.btn_menu_setup_test = QPushButton(self.sub_menu7)
        self.btn_menu_setup_test.setObjectName(u"btn_menu_setup_test")
        sizePolicy.setHeightForWidth(self.btn_menu_setup_test.sizePolicy().hasHeightForWidth())
        self.btn_menu_setup_test.setSizePolicy(sizePolicy)
        self.btn_menu_setup_test.setMinimumSize(QSize(130, 24))
        self.btn_menu_setup_test.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_setup_test.setCheckable(True)
        self.btn_menu_setup_test.setChecked(False)
        self.btn_menu_setup_test.setAutoDefault(False)
        self.btn_menu_setup_test.setFlat(False)

        self.sub_box6_2.addWidget(self.btn_menu_setup_test)

        self.setup_check_box = QWidget(self.sub_menu7)
        self.setup_check_box.setObjectName(u"setup_check_box")
        sizePolicy.setHeightForWidth(self.setup_check_box.sizePolicy().hasHeightForWidth())
        self.setup_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_17 = QVBoxLayout(self.setup_check_box)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.mea_vol = QCheckBox(self.setup_check_box)
        self.mea_vol.setObjectName(u"mea_vol")

        self.verticalLayout_17.addWidget(self.mea_vol)

        self.etc1 = QCheckBox(self.setup_check_box)
        self.etc1.setObjectName(u"etc1")
        sizePolicy1.setHeightForWidth(self.etc1.sizePolicy().hasHeightForWidth())
        self.etc1.setSizePolicy(sizePolicy1)

        self.verticalLayout_17.addWidget(self.etc1)

        self.etc2 = QCheckBox(self.setup_check_box)
        self.etc2.setObjectName(u"etc2")

        self.verticalLayout_17.addWidget(self.etc2)


        self.sub_box6_2.addWidget(self.setup_check_box)


        self.verticalLayout_16.addLayout(self.sub_box6_2)

        self.main_menu2.raise_()
        self.btn_apply.raise_()
        self.btn_cancel.raise_()
        self.main_menu1.raise_()
        self.main_menu3.raise_()
        self.main_menu4.raise_()
        self.sub_menu7.raise_()

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Form)
        self.btn_menu_voltage.toggled.connect(self.vol_check_box.setHidden)
        self.btn_menu_test_mode.toggled.connect(self.tm_check_box.setHidden)
        self.btn_menu_current.toggled.connect(self.curr_check_box.setHidden)
        self.btn_menu_power.toggled.connect(self.pow_check_box.setHidden)
        self.btn_menu_analysis.toggled.connect(self.anal_check_box.setHidden)
        self.btn_menu_system.toggled.connect(self.sys_check_box.setHidden)

        self.btn_menu_voltage.setDefault(True)
        self.btn_menu_test_mode.setDefault(True)
        self.btn_menu_current.setDefault(True)
        self.btn_menu_power.setDefault(True)
        self.btn_menu_analysis.setDefault(True)
        self.btn_menu_system.setDefault(True)
        self.btn_menu_setup_test.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.btn_menu_voltage.setText(QCoreApplication.translate("Form", u"VOLTAGE \u2228", None))
        self.cb_vol_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_vol_rms.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.cb_vol_fund.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.cb_vol_thd.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.cb_vol_freq.setText(QCoreApplication.translate("Form", u"Frequency", None))
        self.cb_vol_residual.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.cb_vol_sliding.setText(QCoreApplication.translate("Form", u"Sliding Ref.", None))
        self.btn_menu_test_mode.setText(QCoreApplication.translate("Form", u"TEST MODE \u2228", None))
        self.cb_tm_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_tm_balance.setText(QCoreApplication.translate("Form", u"Balance", None))
        self.cb_tm_noload.setText(QCoreApplication.translate("Form", u"No Load", None))
        self.btn_menu_current.setText(QCoreApplication.translate("Form", u"CURRENT \u2228", None))
        self.cb_curr_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_curr_rms.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.cb_curr_fund.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.cb_curr_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.cb_curr_thd.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.cb_curr_tdd.setText(QCoreApplication.translate("Form", u"TDD %", None))
        self.cb_curr_cf.setText(QCoreApplication.translate("Form", u"Crest Factor", None))
        self.cb_curr_kf.setText(QCoreApplication.translate("Form", u"K-Factor", None))
        self.cb_curr_residual.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.btn_menu_power.setText(QCoreApplication.translate("Form", u"POWER \u2228", None))
        self.cb_pow_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_pow_p.setText(QCoreApplication.translate("Form", u"Active(P)", None))
        self.cb_pow_q.setText(QCoreApplication.translate("Form", u"Reactive(Q)", None))
        self.cb_pow_s.setText(QCoreApplication.translate("Form", u"Apparent(S)", None))
        self.cb_pow_pf.setText(QCoreApplication.translate("Form", u"PF", None))
        self.cb_pow_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.cb_pow_energy.setText(QCoreApplication.translate("Form", u"Energy", None))
        self.btn_menu_analysis.setText(QCoreApplication.translate("Form", u"ANALYSIS \u2228", None))
        self.cb_anal_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_anal_phasor.setText(QCoreApplication.translate("Form", u"Phasor", None))
        self.cb_anal_harmonics.setText(QCoreApplication.translate("Form", u"Harmonics", None))
        self.cb_anal_waveform.setText(QCoreApplication.translate("Form", u"Waveform", None))
        self.cb_anal_volt_sym.setText(QCoreApplication.translate("Form", u"Volt.Symm.", None))
        self.cb_anal_volt_unbal.setText(QCoreApplication.translate("Form", u"Volt.Unbal.%", None))
        self.cb_anal_curr_sym.setText(QCoreApplication.translate("Form", u"Curr.Symm.", None))
        self.cb_anal_curr_unbal.setText(QCoreApplication.translate("Form", u"Curr.Unbal.%", None))
        self.btn_menu_system.setText(QCoreApplication.translate("Form", u"SYSTEM \u2228", None))
        self.cb_sys_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.btn_menu_setup_test.setText(QCoreApplication.translate("Form", u"SETUP TEST \u2228", None))
        self.mea_vol.setText(QCoreApplication.translate("Form", u"mea_vol", None))
        self.etc1.setText(QCoreApplication.translate("Form", u"Balance", None))
        self.etc2.setText(QCoreApplication.translate("Form", u"No Load", None))
    # retranslateUi

