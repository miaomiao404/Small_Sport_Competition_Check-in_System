# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'matchlist.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.match_list_view = QGraphicsView(self.centralwidget)
        self.match_list_view.setObjectName(u"match_list_view")
        self.match_list_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout.addWidget(self.match_list_view)

        self.function_f = QFrame(self.centralwidget)
        self.function_f.setObjectName(u"function_f")
        self.function_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.function_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.function_f)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.total_match_l = QLabel(self.function_f)
        self.total_match_l.setObjectName(u"total_match_l")
        self.total_match_l.setMinimumSize(QSize(120, 30))
        self.total_match_l.setMaximumSize(QSize(150, 30))

        self.horizontalLayout.addWidget(self.total_match_l)

        self.already_matched_l = QLabel(self.function_f)
        self.already_matched_l.setObjectName(u"already_matched_l")
        self.already_matched_l.setMinimumSize(QSize(120, 30))
        self.already_matched_l.setMaximumSize(QSize(150, 30))

        self.horizontalLayout.addWidget(self.already_matched_l)

        self.total_match_l_3 = QLabel(self.function_f)
        self.total_match_l_3.setObjectName(u"total_match_l_3")
        self.total_match_l_3.setMinimumSize(QSize(120, 30))
        self.total_match_l_3.setMaximumSize(QSize(150, 30))

        self.horizontalLayout.addWidget(self.total_match_l_3)

        self.horizontalSpacer = QSpacerItem(309, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.add_match_btn = QPushButton(self.function_f)
        self.add_match_btn.setObjectName(u"add_match_btn")
        self.add_match_btn.setMinimumSize(QSize(100, 30))
        self.add_match_btn.setMaximumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.add_match_btn)


        self.verticalLayout.addWidget(self.function_f)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8cfd\u4e8b\u5217\u8868", None))
        self.total_match_l.setText(QCoreApplication.translate("MainWindow", u"\u8cfd\u4e8b\u7e3d\u6578\uff1a", None))
        self.already_matched_l.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u5b8c\u6210\u8cfd\u4e8b\u6578\uff1a", None))
        self.total_match_l_3.setText(QCoreApplication.translate("MainWindow", u"\u672a\u5b8c\u6210\u8cfd\u4e8b\u6578\uff1a", None))
        self.add_match_btn.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u589e\u8cfd\u4e8b", None))
    # retranslateUi

