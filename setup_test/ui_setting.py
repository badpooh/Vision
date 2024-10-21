# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
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
        self.widget_2.setGeometry(QRect(20, 20, 161, 531))
        self.widget_2.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 20, 111, 31))
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)
        self.widget_vol_checkBox = QWidget(self.widget_2)
        self.widget_vol_checkBox.setObjectName(u"widget_vol_checkBox")
        self.widget_vol_checkBox.setGeometry(QRect(10, 50, 114, 194))
        self.verticalLayout = QVBoxLayout(self.widget_vol_checkBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox_0 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_0.setObjectName(u"checkBox_0")

        self.verticalLayout.addWidget(self.checkBox_0)

        self.checkBox_1 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_1.setObjectName(u"checkBox_1")

        self.verticalLayout.addWidget(self.checkBox_1)

        self.checkBox_2 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.widget_vol_checkBox)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout.addWidget(self.checkBox_6)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(240, 30, 171, 521))
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(490, 40, 181, 501))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Form)
        self.pushButton.toggled.connect(self.widget_vol_checkBox.setHidden)

        self.pushButton.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"VOLTAGE \u2228", None))
        self.checkBox_0.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.checkBox_1.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.checkBox_4.setText(QCoreApplication.translate("Form", u"Frequency", None))
        self.checkBox_5.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.checkBox_6.setText(QCoreApplication.translate("Form", u"Sliding Ref.", None))
    # retranslateUi

