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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(838, 769)
        Form.setMinimumSize(QSize(800, 600))
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
        self.widget_2.setGeometry(QRect(20, 20, 700, 500))
        self.widget_2.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.menu_voltage = QPushButton(self.widget_2)
        self.menu_voltage.setObjectName(u"menu_voltage")
        self.menu_voltage.setGeometry(QRect(10, 20, 130, 31))
        self.menu_voltage.setCheckable(True)
        self.menu_voltage.setChecked(False)
        self.menu_voltage.setAutoDefault(False)
        self.menu_voltage.setFlat(False)
        self.vol_check_box = QWidget(self.widget_2)
        self.vol_check_box.setObjectName(u"vol_check_box")
        self.vol_check_box.setGeometry(QRect(20, 50, 110, 194))
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

        self.menu_current = QPushButton(self.widget_2)
        self.menu_current.setObjectName(u"menu_current")
        self.menu_current.setGeometry(QRect(140, 20, 130, 31))
        self.menu_current.setCheckable(True)
        self.menu_current.setChecked(False)
        self.menu_current.setAutoDefault(False)
        self.menu_current.setFlat(False)
        self.curr_check_box = QWidget(self.widget_2)
        self.curr_check_box.setObjectName(u"curr_check_box")
        self.curr_check_box.setGeometry(QRect(150, 50, 114, 246))
        self.verticalLayout_2 = QVBoxLayout(self.curr_check_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.curr_all = QCheckBox(self.curr_check_box)
        self.curr_all.setObjectName(u"curr_all")

        self.verticalLayout_2.addWidget(self.curr_all)

        self.curr_rms = QCheckBox(self.curr_check_box)
        self.curr_rms.setObjectName(u"curr_rms")

        self.verticalLayout_2.addWidget(self.curr_rms)

        self.curr_fund = QCheckBox(self.curr_check_box)
        self.curr_fund.setObjectName(u"curr_fund")

        self.verticalLayout_2.addWidget(self.curr_fund)

        self.curr_demand = QCheckBox(self.curr_check_box)
        self.curr_demand.setObjectName(u"curr_demand")

        self.verticalLayout_2.addWidget(self.curr_demand)

        self.curr_thd = QCheckBox(self.curr_check_box)
        self.curr_thd.setObjectName(u"curr_thd")

        self.verticalLayout_2.addWidget(self.curr_thd)

        self.curr_tdd = QCheckBox(self.curr_check_box)
        self.curr_tdd.setObjectName(u"curr_tdd")

        self.verticalLayout_2.addWidget(self.curr_tdd)

        self.curr_crest_factor = QCheckBox(self.curr_check_box)
        self.curr_crest_factor.setObjectName(u"curr_crest_factor")

        self.verticalLayout_2.addWidget(self.curr_crest_factor)

        self.curr_k_factor = QCheckBox(self.curr_check_box)
        self.curr_k_factor.setObjectName(u"curr_k_factor")

        self.verticalLayout_2.addWidget(self.curr_k_factor)

        self.curr_residual = QCheckBox(self.curr_check_box)
        self.curr_residual.setObjectName(u"curr_residual")

        self.verticalLayout_2.addWidget(self.curr_residual)

        self.menu_power = QPushButton(self.widget_2)
        self.menu_power.setObjectName(u"menu_power")
        self.menu_power.setGeometry(QRect(270, 20, 130, 31))
        self.menu_power.setCheckable(True)
        self.menu_power.setChecked(False)
        self.menu_power.setAutoDefault(False)
        self.menu_power.setFlat(False)
        self.pow_check_box = QWidget(self.widget_2)
        self.pow_check_box.setObjectName(u"pow_check_box")
        self.pow_check_box.setGeometry(QRect(280, 50, 114, 246))
        self.verticalLayout_3 = QVBoxLayout(self.pow_check_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pow_all = QCheckBox(self.pow_check_box)
        self.pow_all.setObjectName(u"pow_all")

        self.verticalLayout_3.addWidget(self.pow_all)

        self.pow_p = QCheckBox(self.pow_check_box)
        self.pow_p.setObjectName(u"pow_p")

        self.verticalLayout_3.addWidget(self.pow_p)

        self.pow_q = QCheckBox(self.pow_check_box)
        self.pow_q.setObjectName(u"pow_q")

        self.verticalLayout_3.addWidget(self.pow_q)

        self.pow_s = QCheckBox(self.pow_check_box)
        self.pow_s.setObjectName(u"pow_s")

        self.verticalLayout_3.addWidget(self.pow_s)

        self.pow_pf = QCheckBox(self.pow_check_box)
        self.pow_pf.setObjectName(u"pow_pf")

        self.verticalLayout_3.addWidget(self.pow_pf)

        self.pow_demand = QCheckBox(self.pow_check_box)
        self.pow_demand.setObjectName(u"pow_demand")

        self.verticalLayout_3.addWidget(self.pow_demand)

        self.pow_energy = QCheckBox(self.pow_check_box)
        self.pow_energy.setObjectName(u"pow_energy")

        self.verticalLayout_3.addWidget(self.pow_energy)

        self.menu_analysis = QPushButton(self.widget_2)
        self.menu_analysis.setObjectName(u"menu_analysis")
        self.menu_analysis.setGeometry(QRect(400, 20, 130, 31))
        self.menu_analysis.setCheckable(True)
        self.menu_analysis.setChecked(False)
        self.menu_analysis.setAutoDefault(False)
        self.menu_analysis.setFlat(False)
        self.anal_check_box = QWidget(self.widget_2)
        self.anal_check_box.setObjectName(u"anal_check_box")
        self.anal_check_box.setGeometry(QRect(410, 50, 114, 246))
        self.verticalLayout_4 = QVBoxLayout(self.anal_check_box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.anal_all = QCheckBox(self.anal_check_box)
        self.anal_all.setObjectName(u"anal_all")

        self.verticalLayout_4.addWidget(self.anal_all)

        self.anal_phasor = QCheckBox(self.anal_check_box)
        self.anal_phasor.setObjectName(u"anal_phasor")

        self.verticalLayout_4.addWidget(self.anal_phasor)

        self.anal_harmonics = QCheckBox(self.anal_check_box)
        self.anal_harmonics.setObjectName(u"anal_harmonics")

        self.verticalLayout_4.addWidget(self.anal_harmonics)

        self.anal_waveform = QCheckBox(self.anal_check_box)
        self.anal_waveform.setObjectName(u"anal_waveform")

        self.verticalLayout_4.addWidget(self.anal_waveform)

        self.anal_vol_symm = QCheckBox(self.anal_check_box)
        self.anal_vol_symm.setObjectName(u"anal_vol_symm")

        self.verticalLayout_4.addWidget(self.anal_vol_symm)

        self.anal_vol_unbal = QCheckBox(self.anal_check_box)
        self.anal_vol_unbal.setObjectName(u"anal_vol_unbal")

        self.verticalLayout_4.addWidget(self.anal_vol_unbal)

        self.anal_curr_symm = QCheckBox(self.anal_check_box)
        self.anal_curr_symm.setObjectName(u"anal_curr_symm")

        self.verticalLayout_4.addWidget(self.anal_curr_symm)

        self.anal_curr_unbal = QCheckBox(self.anal_check_box)
        self.anal_curr_unbal.setObjectName(u"anal_curr_unbal")

        self.verticalLayout_4.addWidget(self.anal_curr_unbal)

        self.btn_apply = QPushButton(self.widget_2)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setGeometry(QRect(520, 450, 75, 24))
        self.btn_cancel = QPushButton(self.widget_2)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(605, 450, 75, 24))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Form)
        self.menu_voltage.toggled.connect(self.vol_check_box.setHidden)
        self.menu_current.toggled.connect(self.curr_check_box.setHidden)
        self.menu_power.toggled.connect(self.pow_check_box.setHidden)
        self.menu_analysis.toggled.connect(self.anal_check_box.setHidden)

        self.menu_voltage.setDefault(True)
        self.menu_current.setDefault(True)
        self.menu_power.setDefault(True)
        self.menu_analysis.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.menu_voltage.setText(QCoreApplication.translate("Form", u"VOLTAGE \u2228", None))
        self.cb_vol_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_vol_rms.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.cb_vol_fund.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.cb_vol_thd.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.cb_vol_freq.setText(QCoreApplication.translate("Form", u"Frequency", None))
        self.cb_vol_residual.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.cb_vol_sliding.setText(QCoreApplication.translate("Form", u"Sliding Ref.", None))
        self.menu_current.setText(QCoreApplication.translate("Form", u"CURRENT \u2228", None))
        self.curr_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.curr_rms.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.curr_fund.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.curr_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.curr_thd.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.curr_tdd.setText(QCoreApplication.translate("Form", u"TDD %", None))
        self.curr_crest_factor.setText(QCoreApplication.translate("Form", u"Crest Factor", None))
        self.curr_k_factor.setText(QCoreApplication.translate("Form", u"K-Factor", None))
        self.curr_residual.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.menu_power.setText(QCoreApplication.translate("Form", u"POWER \u2228", None))
        self.pow_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.pow_p.setText(QCoreApplication.translate("Form", u"Active(P)", None))
        self.pow_q.setText(QCoreApplication.translate("Form", u"Reactive(Q)", None))
        self.pow_s.setText(QCoreApplication.translate("Form", u"Apparent(S)", None))
        self.pow_pf.setText(QCoreApplication.translate("Form", u"PF", None))
        self.pow_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.pow_energy.setText(QCoreApplication.translate("Form", u"Energy", None))
        self.menu_analysis.setText(QCoreApplication.translate("Form", u"ANALYSIS \u2228", None))
        self.anal_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.anal_phasor.setText(QCoreApplication.translate("Form", u"Phasor", None))
        self.anal_harmonics.setText(QCoreApplication.translate("Form", u"Harmonics", None))
        self.anal_waveform.setText(QCoreApplication.translate("Form", u"Waveform", None))
        self.anal_vol_symm.setText(QCoreApplication.translate("Form", u"Volt.Symm.", None))
        self.anal_vol_unbal.setText(QCoreApplication.translate("Form", u"Volt.Unbal.%", None))
        self.anal_curr_symm.setText(QCoreApplication.translate("Form", u"Curr.Symm.", None))
        self.anal_curr_unbal.setText(QCoreApplication.translate("Form", u"Curr.Unbal.%", None))
        self.btn_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

