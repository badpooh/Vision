# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_ocr_setting.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QPushButton, QSizePolicy,
    QWidget)

class Ui_OCR_SETTING(object):
    def setupUi(self, OCR_SETTING):
        if not OCR_SETTING.objectName():
            OCR_SETTING.setObjectName(u"OCR_SETTING")
        OCR_SETTING.resize(935, 635)
        self.btn_save = QPushButton(OCR_SETTING)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(250, 50, 75, 24))
        self.btn_load = QPushButton(OCR_SETTING)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setGeometry(QRect(250, 100, 75, 24))
        self.check_box_1 = QCheckBox(OCR_SETTING)
        self.check_box_1.setObjectName(u"check_box_1")
        self.check_box_1.setGeometry(QRect(30, 40, 100, 20))
        self.check_box_2 = QCheckBox(OCR_SETTING)
        self.check_box_2.setObjectName(u"check_box_2")
        self.check_box_2.setGeometry(QRect(30, 90, 100, 20))
        self.check_box_3 = QCheckBox(OCR_SETTING)
        self.check_box_3.setObjectName(u"check_box_3")
        self.check_box_3.setGeometry(QRect(30, 140, 100, 20))
        self.check_box_4 = QCheckBox(OCR_SETTING)
        self.check_box_4.setObjectName(u"check_box_4")
        self.check_box_4.setGeometry(QRect(30, 190, 110, 20))

        self.retranslateUi(OCR_SETTING)

        QMetaObject.connectSlotsByName(OCR_SETTING)
    # setupUi

    def retranslateUi(self, OCR_SETTING):
        OCR_SETTING.setWindowTitle(QCoreApplication.translate("OCR_SETTING", u"Form", None))
        self.btn_save.setText(QCoreApplication.translate("OCR_SETTING", u"SAVE", None))
        self.btn_load.setText(QCoreApplication.translate("OCR_SETTING", u"LOAD", None))
        self.check_box_1.setText(QCoreApplication.translate("OCR_SETTING", u"VOLTAGE L-L", None))
        self.check_box_2.setText(QCoreApplication.translate("OCR_SETTING", u"VOLTAGE L-N", None))
        self.check_box_3.setText(QCoreApplication.translate("OCR_SETTING", u"CURRENT RMS", None))
        self.check_box_4.setText(QCoreApplication.translate("OCR_SETTING", u"CURRENT Fund.", None))
    # retranslateUi

