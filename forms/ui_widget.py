# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QSizePolicy, QWidget)


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.setWindowModality(Qt.NonModal)
        Widget.resize(350, 150)
        Widget.setMinimumSize(QSize(350, 150))
        Widget.setMaximumSize(QSize(350, 150))
        Widget.setFocusPolicy(Qt.ClickFocus)
        Widget.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u"src/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        Widget.setAutoFillBackground(True)
        self.progressBar = QProgressBar(Widget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(0, 120, 350, 30))
        self.progressBar.setInputMethodHints(Qt.ImhNone)
        self.progressBar.setValue(50)
        self.progressBar.setTextVisible(False)
        self.lineEdit_Url = QLineEdit(Widget)
        self.lineEdit_Url.setObjectName(u"lineEdit_Url")
        self.lineEdit_Url.setGeometry(QRect(0, 20, 350, 30))
        self.pushButton_Error = QPushButton(Widget)
        self.pushButton_Error.setObjectName(u"pushButton_Error")
        self.pushButton_Error.setGeometry(QRect(0, 50, 170, 50))
        self.pushButton_Time = QPushButton(Widget)
        self.pushButton_Time.setObjectName(u"pushButton_Time")
        self.pushButton_Time.setGeometry(QRect(180, 50, 170, 50))
        self.label_main = QLabel(Widget)
        self.label_main.setObjectName(u"label_main")
        self.label_main.setGeometry(QRect(115, 0, 120, 20))
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setStrikeOut(False)
        font.setKerning(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label_main.setFont(font)
        self.label_Status = QLabel(Widget)
        self.label_Status.setObjectName(u"label_Status")
        self.label_Status.setGeometry(QRect(0, 100, 350, 16))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"SQLI Tester", None))
        self.lineEdit_Url.setPlaceholderText(QCoreApplication.translate("Widget", u"Type  here URL ", None))
        self.pushButton_Error.setText(QCoreApplication.translate("Widget", u"Error-based\n"
                                                                           "Test", None))
        # if QT_CONFIG(shortcut)
        self.pushButton_Error.setShortcut(QCoreApplication.translate("Widget", u"Shift+Return", None))
        # endif // QT_CONFIG(shortcut)
        self.pushButton_Time.setText(QCoreApplication.translate("Widget", u"Time-based\n"
                                                                          "Test", None))
        # if QT_CONFIG(shortcut)
        self.pushButton_Time.setShortcut(QCoreApplication.translate("Widget", u"Return", None))
        # endif // QT_CONFIG(shortcut)
        self.label_main.setText(QCoreApplication.translate("Widget", u"SQL Injection tester", None))
        self.label_Status.setText(QCoreApplication.translate("Widget", u"Status: Nothing", None))
    # retranslateUi
