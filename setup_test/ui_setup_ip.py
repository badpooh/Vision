# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setup_ip.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_setup_ip(object):
    def setupUi(self, setup_ip):
        if not setup_ip.objectName():
            setup_ip.setObjectName(u"setup_ip")
        setup_ip.resize(400, 300)
        self.widget = QWidget(setup_ip)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 400, 300))
        self.widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.btn_ip_add = QPushButton(self.widget)
        self.btn_ip_add.setObjectName(u"btn_ip_add")
        self.btn_ip_add.setGeometry(QRect(260, 30, 75, 24))
        self.btn_ip_select = QPushButton(self.widget)
        self.btn_ip_select.setObjectName(u"btn_ip_select")
        self.btn_ip_select.setGeometry(QRect(260, 120, 75, 24))
        self.btn_ip_del = QPushButton(self.widget)
        self.btn_ip_del.setObjectName(u"btn_ip_del")
        self.btn_ip_del.setGeometry(QRect(260, 70, 75, 24))
        self.ip_typing = QLineEdit(self.widget)
        self.ip_typing.setObjectName(u"ip_typing")
        self.ip_typing.setGeometry(QRect(40, 30, 151, 31))
        self.ip_list = QTableWidget(self.widget)
        if (self.ip_list.columnCount() < 1):
            self.ip_list.setColumnCount(1)
        self.ip_list.setObjectName(u"ip_list")
        self.ip_list.setGeometry(QRect(40, 90, 151, 191))
        self.ip_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ip_list.setRowCount(0)
        self.ip_list.setColumnCount(1)
        self.ip_list.horizontalHeader().setVisible(True)

        self.retranslateUi(setup_ip)

        QMetaObject.connectSlotsByName(setup_ip)
    # setupUi

    def retranslateUi(self, setup_ip):
        setup_ip.setWindowTitle(QCoreApplication.translate("setup_ip", u"Form", None))
        self.btn_ip_add.setText(QCoreApplication.translate("setup_ip", u"Add", None))
        self.btn_ip_select.setText(QCoreApplication.translate("setup_ip", u"Select", None))
        self.btn_ip_del.setText(QCoreApplication.translate("setup_ip", u"Del", None))
    # retranslateUi

